//#####################################################################
//#                All rights reserved to davekolian                  #
//#####################################################################

const { MongoClient, ServerApiVersion } = require('mongodb');
const express = require('express');

const puppeteer = require('puppeteer-extra');
// add stealth plugin and use defaults (all evasion techniques)
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const stealth = StealthPlugin();
stealth.enabledEvasions.delete('chrome.runtime');
stealth.enabledEvasions.delete('iframe.contentWindow');
puppeteer.use(stealth);

import chromium from '@sparticuz/chromium';
chromium.setHeadlessMode = true;
chromium.setGraphicsMode = false;
let new_chapters = [];
let record_ids = 0;

async function pageInterception(page, domain) {
	if (domain == 'manhuaplus') {
		await page.setRequestInterception(true);

		page.on('request', (req) => {
			if (
				req.resourceType() == 'stylesheet' ||
				req.resourceType() == 'font' ||
				req.resourceType() == 'image'
			) {
				req.abort();
			} else {
				req.continue();
			}
		});
	} else if (
		domain == 'reaperscans' ||
		domain == 'asurascans' ||
		domain == 'earlym'
	) {
		await page.setRequestInterception(true);

		page.on('request', (req) => {
			if (
				req.resourceType() == 'stylesheet' ||
				req.resourceType() == 'font' ||
				req.resourceType() == 'image' ||
				req.resourceType() == 'script'
			) {
				req.abort();
			} else {
				req.continue();
			}
		});
	}
}

async function mainScrapers(objs) {
	let browser = await puppeteer.launch({
		args: chromium.args,
		defaultViewport: chromium.defaultViewport,
		executablePath:
			process.env.CHROME_EXECUTABLE_PATH ||
			(await chromium.executablePath(
				'/var/task/node_modules/@sparticuz/chromium/bin'
			)),
	});

	for (let obj of objs) {
		if (obj.update === true) {
			let url = obj.url;
			let last_read = obj.last_read;
			let domain = '';
			let split = url.split('//')[1].split('.');
			if (split[0] == 'www') {
				domain = split[1];
			} else {
				domain = split[0];
			}

			let page = await browser.newPage();

			if (domain == 'manhuaplus') {
				await pageInterception(page, domain);
				await getFromMP(page, url, last_read);
			} else if (domain == 'reaperscans') {
				await pageInterception(page, domain);
				await getFromReaper(page, url, last_read);
			} else if (domain == 'asurascans') {
				await pageInterception(page, domain);
				await getFromAsura(page, url, last_read);
			} else if (domain == 'earlym') {
				await pageInterception(page, domain);
				await getFromEarly(page, url, last_read);
			} else if (domain == 'mangakakalot') {
				await pageInterception(page, domain);
				await getFromMangakakalot(page, url, last_read);
			} else if (domain == 'chapmanganato') {
				await pageInterception(page, domain);
				await getFromManganato(page, url, last_read);
			}

			await page.close();
		}
	}

	await browser.close();
}

async function getFromMP(page, url, last_read) {
	const local_chapters = [];
	const local_links = [];

	try {
		await page.goto(url, { timeout: 0 });
		//await new Promise((r) => setTimeout(r, 10000));

		let name = await page.evaluate(() => {
			let x = document.getElementsByTagName('h1');

			return x[0].innerText;
		});
		console.log('Reading: ' + name);

		let img_link = await page.evaluate(() => {
			let x = document.getElementsByClassName('summary_image');
			let link = x[0].children[0].children[0].dataset.src.slice(0, -12);
			let ext = x[0].children[0].children[0].dataset.src.slice(-4);

			let final_link = link + ext;
			return final_link;
		});

		let arr = await page.evaluate((last_read) => {
			let x = document.getElementsByClassName('wp-manga-chapter');
			console.log(x);
			let arr = [];
			let top = Number(x[0].innerText.split('\n')[0].split(' ')[1]);
			for (let i = 0; i < top - last_read; i++) {
				let chap_no = x[i].innerText.split('\n')[0].split(' ')[1];
				let date = x[i].innerText.split('\n')[1];
				arr.push([chap_no, date, x[i].children[0].href]);
			}

			return arr;
		}, last_read);

		for (let chap of arr) {
			local_chapters.push(chap[0]);
			local_links.push(chap[2]);
		}

		if (local_chapters.length > 0) {
			new_document = {
				record_id: record_ids,
				url: url,
				manga_name: name,
				manga_chapters: local_chapters,
				img_link_bg: img_link,
				chapter_links: local_links,
				last_read: last_read,
			};
			record_ids += 1;

			console.log(new_document);
			new_chapters.push(new_document);
		}

		console.log('Done reading above');
	} catch (error) {
		console.log('Something wrong with reading this ManhuaPlus page');
		console.log(error);
	}
}

function cleanReaperChapters(arr_split) {
	let t = 1;

	if (isNaN(Number(arr_split[t].replace(/[()]/g, '')))) {
		t = arr_split.length - 1;
	}

	let top = arr_split[t].replace(/[()]/g, '');
	return top;
}

async function getFromReaper(page, url, last_read) {
	const local_chapters = [];
	const local_links = [];

	try {
		await page.goto(url, { timeout: 0 });
		// await new Promise((r) => setTimeout(r, 10000));

		let name = await page.evaluate(() => {
			let x = document.getElementsByTagName('h1');

			return x[0].innerText;
		});
		console.log('Reading: ' + name);

		let img_link = await page.evaluate(() => {
			let x = document.getElementsByClassName('summary_image');
			let link = x[0].children[0].children[0].dataset.src;

			return link;
		});

		await page.exposeFunction('cleanReaperChapters', cleanReaperChapters);

		let arr = await page.evaluate(async (last_read) => {
			let x = document.getElementsByClassName('wp-manga-chapter');
			console.log(x);
			let arr = [];
			let top_arr =
				x[0].children[1].children[0].children[0].innerText.split(' ');
			let top = await cleanReaperChapters(top_arr);

			for (let i = 0; i < top - last_read; i++) {
				let chapter_arr =
					x[i].children[1].children[0].children[0].innerText.split(' ');
				let chap_no = await cleanReaperChapters(chapter_arr);

				let date = x[i].children[1].children[0].children[1].innerText;
				let link = x[i].children[1].children[0].href;
				arr.push([chap_no, date, link]);
			}

			return arr;
		}, last_read);

		for (let chap of arr) {
			local_chapters.push(chap[0]);
			local_links.push(chap[2]);
		}

		if (local_chapters.length > 0) {
			new_document = {
				record_id: record_ids,
				url: url,
				manga_name: name,
				manga_chapters: local_chapters,
				img_link_bg: img_link,
				chapter_links: local_links,
				last_read: last_read,
			};
			record_ids += 1;
			console.log(new_document);
			new_chapters.push(new_document);
		}

		console.log('Done reading above');
	} catch (error) {
		console.log('Error reading this ReaperScans page');
		console.log(error);
	}
}

async function getFromEarly(page, url, last_read) {
	const local_chapters = [];
	const local_links = [];

	try {
		await page.goto(url, { timeout: 0 });
		// await new Promise((r) => setTimeout(r, 10000));

		let name = await page.evaluate(() => {
			let x = document.getElementsByClassName('mx-1');

			return x[0].innerText;
		});
		console.log('Reading: ' + name);

		let img_link = await page.evaluate(() => {
			let x = document.getElementsByClassName('manga-page-img');
			let link = x[0].src;

			return link;
		});

		let arr = await page.evaluate((last_read) => {
			let x = document.getElementsByClassName('chapter-row');
			console.log(x);
			let arr = [];
			let top = Number(
				x[2].children[1].children[0].children[0].innerText
					.split('\n')[0]
					.split(' ')[1]
			);

			for (let i = 2; i < (top - last_read) * 2 + 2; i += 2) {
				let chap_no = x[i].children[1].children[0].children[0].innerText
					.split('\n')[0]
					.split(' ')[1];
				let date = x[i].children[3].title.split(' ')[0];
				arr.push([chap_no, date, x[i].children[1].children[0].href]);
			}

			print(arr);

			return arr;
		}, last_read);

		for (let chap of arr) {
			local_chapters.push(chap[0]);
			local_links.push(chap[2]);
		}

		if (local_chapters.length > 0) {
			new_document = {
				record_id: record_ids,
				url: url,
				manga_name: name,
				manga_chapters: local_chapters,
				img_link_bg: img_link,
				chapter_links: local_links,
				last_read: last_read,
			};
			record_ids += 1;

			console.log(new_document);
			new_chapters.push(new_document);
		}

		console.log('Done reading above');
	} catch (error) {
		console.log('Something wrong with reading this EarlyM page');
		console.log(error);
	}
}

async function getFromMangakakalot(page, url, last_read) {
	const local_chapters = [];
	const local_links = [];

	try {
		await page.goto(url, { timeout: 0 });
		// await new Promise((r) => setTimeout(r, 10000));

		let name = await page.evaluate(() => {
			let x = document.getElementsByTagName('h1');

			return x[0].innerText;
		});
		console.log('Reading: ' + name);

		let img_link = await page.evaluate(() => {
			let x = document.getElementsByClassName('manga-info-pic');
			let link = x[0].children[0].src;

			return link;
		});

		let arr = await page.evaluate((last_read) => {
			let x = document.getElementsByClassName('row');
			console.log(x);
			let arr = [];
			let _len_top = x[1].children[0].innerText.length;
			let top = Number(
				x[1].children[0].innerText
					.slice(_len_top - 4, _len_top)
					.replace(/\D/g, '')
			);

			for (let i = 1; i < top - last_read; i += 1) {
				let _len = x[i].children[0].innerText.length;
				let chap_no = Number(
					x[i].children[0].innerText.slice(_len - 4, _len).replace(/\D/g, '')
				);
				let date = x[i].children[2].title.split(' ')[0];
				let ch_link = x[i].children[0].children[0].href;
				// console.log(chap_no, date, ch_link);
				arr.push([chap_no, date, ch_link]);
			}

			return arr;
		}, last_read);

		for (let chap of arr) {
			local_chapters.push(chap[0]);
			local_links.push(chap[2]);
		}

		if (local_chapters.length > 0) {
			new_document = {
				record_id: record_ids,
				url: url,
				manga_name: name,
				manga_chapters: local_chapters,
				img_link_bg: img_link,
				chapter_links: local_links,
				last_read: last_read,
			};
			record_ids += 1;

			console.log(new_document);
			new_chapters.push(new_document);
		}

		console.log('Done reading above');
	} catch (error) {
		console.log('Something wrong with reading this Mangakakalot page');
		console.log(error);
	}
}

async function getFromManganato(page, url, last_read) {
	const local_chapters = [];
	const local_links = [];

	try {
		await page.goto(url, { timeout: 0 });
		// await new Promise((r) => setTimeout(r, 10000));

		let name = await page.evaluate(() => {
			let x = document.getElementsByTagName('h1');

			return x[0].innerText;
		});
		console.log('Reading: ' + name);

		let img_link = await page.evaluate(() => {
			let x = document.getElementsByClassName('info-image');
			let link = x[0].children[0].src;

			return link;
		});

		let arr = await page.evaluate((last_read) => {
			let x = document.getElementsByClassName('row-content-chapter')[0]
				.children;
			console.log(x);
			let arr = [];
			let _len_top = x[0].children[0].innerText.length;
			let top = Number(
				x[0].children[0].innerText
					.slice(_len_top - 4, _len_top)
					.replace(/\D/g, '')
			);

			for (let i = 0; i < top - last_read; i += 1) {
				let _len = x[i].children[0].innerText.length;
				let chap_no = Number(
					x[i].children[0].innerText.slice(_len - 4, _len).replace(/\D/g, '')
				);
				let date = x[i].children[2].title.slice(0, 11);
				let ch_link = x[i].children[0].href;
				// console.log(chap_no, date, ch_link);
				arr.push([chap_no, date, ch_link]);
			}

			return arr;
		}, last_read);

		for (let chap of arr) {
			local_chapters.push(chap[0]);
			local_links.push(chap[2]);
		}

		if (local_chapters.length > 0) {
			new_document = {
				record_id: record_ids,
				url: url,
				manga_name: name,
				manga_chapters: local_chapters,
				img_link_bg: img_link,
				chapter_links: local_links,
				last_read: last_read,
			};
			record_ids += 1;

			console.log(new_document);
			new_chapters.push(new_document);
		}

		console.log('Done reading above');
	} catch (error) {
		console.log('Something wrong with reading this Mangakakalot page');
		console.log(error);
	}
}

async function getFromAsura(page, url, last_read) {
	const local_chapters = [];
	const local_links = [];

	try {
		await page.goto(url, { timeout: 0 });
		//await new Promise((r) => setTimeout(r, 10000));

		let name = await page.evaluate(() => {
			let x = document.getElementsByTagName('h1');

			return x[0].innerText;
		});
		console.log('Reading: ' + name);

		let img_link = await page.evaluate(() => {
			let x = document.getElementsByClassName('wp-post-image');
			let link = x[0].src;

			return link;
		});
		console.log(img_link);

		let arr = await page.evaluate((last_read) => {
			console.log('here');
			let x = document.getElementsByClassName('eph-num');
			console.log(x);
			let arr = [];
			let top = Number(x[0].children[0].children[0].innerText.split(' ')[1]);

			for (let i = 0; i < top - last_read; i++) {
				let chap_no = x[i].children[0].children[0].innerText.split(' ')[1];
				let date = x[i].children[0].children[1].innerText;
				let link = x[i].children[0].href;
				arr.push([chap_no, date, link]);
			}

			return arr;
		}, last_read);

		for (let chap of arr) {
			local_chapters.push(chap[0]);
			local_links.push(chap[2]);
		}

		if (local_chapters.length > 0) {
			new_document = {
				record_id: record_ids,
				url: url,
				manga_name: name,
				manga_chapters: local_chapters,
				img_link_bg: img_link,
				chapter_links: local_links,
				last_read: last_read,
			};
			record_ids += 1;

			console.log(new_document);
			new_chapters.push(new_document);
		}

		console.log('Done reading above');
	} catch (error) {
		console.log('Error reading this AsuraScans page');
		console.log(error);
	}
}

async function getURLs() {
	const uri = process.env.CONNECTION_URL;
	const db = process.env.MANGAS_DB;
	const col = process.env.MANGAS_URL_COL;

	try {
		const client = new MongoClient(uri, {
			serverApi: {
				version: ServerApiVersion.v1,
				strict: true,
				deprecationErrors: true,
			},
		});

		await client.connect();
		const collection = client.db(db).collection(col);
		const data = await collection.find({}).toArray();

		client.close();
		// console.log(data);

		return data;
	} catch (error) {
		console.log('Error in reading the URL DB');
		console.log(error);
	}
}

async function pushNewToDB(newData) {
	const uri = process.env.CONNECTION_URL;
	const db = process.env.MANGAS_DB;
	const col = process.env.MANGAS_ALL_COL;

	try {
		const client = new MongoClient(uri, {
			serverApi: {
				version: ServerApiVersion.v1,
				strict: true,
				deprecationErrors: true,
			},
		});
		await client.connect();
		const collection = client.db(db).collection(col);

		await collection.deleteMany({});
		await collection.insertMany(newData);

		client.close();

		console.log('Completed updating DB');
	} catch (error) {
		console.log('Error in connecting to MANGAS DB');
		console.log(error);
	}
}

async function test() {
	let browser = await puppeteer.launch({ headless: true });
	let page = await browser.newPage();
	await page.goto('https://mangakakalot.com/manga/wo929163', { timeout: 0 });
	let name = await page.evaluate(() => {
		let x = document.getElementsByTagName('h1');

		return x[0].innerText;
	});
	await page.close();
	await browser.close;

	return name;
}

async function main() {
	while (true) {
		record_ids = 0;

		console.log('Starting the process...');

		// let name = await test();
		// console.log(name);
		const data = await getURLs();
		await mainScrapers(data);
		if (new_chapters.length > 0) {
			await pushNewToDB(new_chapters);
			new_chapters = [];
		}

		let sleep = 12000 * 60 * 60;
		console.log('Sleep for a 12 hours');
		await new Promise((r) => setTimeout(r, sleep));
	}
}

// main();

exports.handler = async () => {
	try {
		await main();
		return {
			statusCode: 200,
			body: 'Scraping completed successfully!',
		};
	} catch (error) {
		console.error('Scraping failed:', error);
		return {
			statusCode: 500,
			body: 'An error occurred during scraping.',
		};
	}
};
