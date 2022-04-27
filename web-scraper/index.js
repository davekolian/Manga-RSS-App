//#####################################################################
//#                All rights reserved to davekolian                  #
//#####################################################################

require('dotenv').config();
const { MongoClient, ServerApiVersion } = require('mongodb');
const express = require('express');

const puppeteer = require('puppeteer-extra');
// add stealth plugin and use defaults (all evasion techniques)
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const stealth = StealthPlugin();
stealth.enabledEvasions.delete('chrome.runtime');
stealth.enabledEvasions.delete('iframe.contentWindow');
puppeteer.use(stealth);

const new_chapters = [];
let record_ids = 0;

async function mainScrapers(objs) {
	let browser = await puppeteer.launch({ headless: true });

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

			//await page.setRequestInterception(true);
			//await page.setDefaultNavigationTimeout(0);

			// page.on('request', (req) => {
			// 	if (
			// 		req.resourceType() == 'stylesheet' ||
			// 		req.resourceType() == 'font' ||
			// 		req.resourceType() == 'image' ||
			// 		req.resourceType() == 'script'
			// 	) {
			// 		req.abort();
			// 	} else {
			// 		req.continue();
			// 	}
			// });

			if (domain == 'manhuaplus') await getFromMP(page, url, last_read);
			else if (domain == 'reaperscans')
				await getFromReaper(page, url, last_read);
			else if (domain == 'asurascans') await getFromAsura(page, url, last_read);
			//else if (domain == 'earlym') await get_from_Early(page, url);

			await page.close();
		}
	}

	await browser.close();
}

async function getFromMP(page, url, last_read) {
	const local_chapters = [];
	const local_links = [];

	await page.goto(url);

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

	let arr = await page.evaluate(() => {
		let x = document.getElementsByClassName('wp-manga-chapter');
		console.log(x);
		let arr = [];
		let chap_no = 10;
		for (let i = 0; i < chap_no; i++) {
			let chapter = x[i].innerText.split(' ').slice(0, 2).join(' ');
			chap_no = chapter.split(' ')[1];

			let date = x[i].innerText.split(' ').slice(2).join(' ');
			arr.push([chap_no, date, x[i].children[0].href]);
		}

		return arr;
	});

	for (let chap of arr) {
		if (chap[0] > last_read) {
			local_chapters.push(chap[0]);
			local_links.push(chap[2]);
		}
	}

	if (local_chapters.length > 0) {
		new_document = {
			record_id: record_ids,
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
}

async function getFromReaper(page, url, last_read) {
	const local_chapters = [];
	const local_links = [];

	await page.goto(url);
	await new Promise((r) => setTimeout(r, 10000));

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

	let arr = await page.evaluate(() => {
		let x = document.getElementsByClassName('wp-manga-chapter');
		console.log(x);
		let arr = [];
		let chap_no = 10;
		for (let i = 0; i < chap_no; i++) {
			let chapter = x[i].children[1].children[0].children[0].innerText;

			if (chapter.includes('S2')) {
				// Mainly for GOB
				clean_chapt = chapter.split(' - ')[1].replace(/[()]/g, '');
				chap_no = clean_chapt.split(' ')[1];
			} else {
				chap_no = chapter.split(' ')[1];
			}

			let date = x[i].children[1].children[0].children[1].innerText;
			let link = x[i].children[1].children[0].href;
			arr.push([chap_no, date, link]);
		}

		return arr;
	});

	for (let chap of arr) {
		if (chap[0] > last_read) {
			local_chapters.push(chap[0]);
			local_links.push(chap[2]);
		}
	}

	if (local_chapters.length > 0) {
		new_document = {
			record_id: record_ids,
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
}

async function get_from_Early(page, url) {
	//Do later
}

async function getFromAsura(page, url, last_read) {
	const local_chapters = [];
	const local_links = [];

	await page.goto(url);
	await new Promise((r) => setTimeout(r, 10000));

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

	let arr = await page.evaluate(() => {
		let x = document.getElementsByClassName('eph-num');
		console.log(x);
		let arr = [];
		let chap_no = 10;
		for (let i = 0; i < chap_no; i++) {
			let chapter = x[i].children[0].children[0].innerText;
			chap_no = chapter.split(' ')[1];

			let date = x[i].children[0].children[1].innerText;
			let link = x[i].children[0].href;
			arr.push([chap_no, date, link]);
		}

		return arr;
	});

	for (let chap of arr) {
		if (chap[0] > last_read) {
			local_chapters.push(chap[0]);
			local_links.push(chap[2]);
		}
	}

	if (local_chapters.length > 0) {
		new_document = {
			record_id: record_ids,
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
}

async function getURLs() {
	const uri = process.env.CONNECTION_URL;
	const db = process.env.MANGAS_DB;
	const col = process.env.MANGAS_URL_COL;

	const client = new MongoClient(uri, {
		useNewUrlParser: true,
		useUnifiedTopology: true,
		serverApi: ServerApiVersion.v1,
	});

	await client.connect();
	const collection = client.db(db).collection(col);
	const data = await collection.find({}).toArray();

	client.close();

	return data;
}

async function pushNewToDB(newData) {
	const uri = process.env.CONNECTION_URL;
	const db = process.env.MANGAS_DB;
	const col = process.env.MANGAS_ALL_COL;

	const client = new MongoClient(uri, {
		useNewUrlParser: true,
		useUnifiedTopology: true,
		serverApi: ServerApiVersion.v1,
	});

	await client.connect();
	const collection = client.db(db).collection(col);

	await collection.deleteMany({});
	await collection.insertMany(newData);

	client.close();

	console.log('Completed updating DB');
}

async function main() {
	while (true) {
		record_ids = 0;
		console.log('Starting the process...');
		const data = await getURLs();
		await mainScrapers(data);
		await pushNewToDB(new_chapters);

		let sleep = 1000 * 60 * 60;
		console.log('Sleep for an hour');
		await new Promise((r) => setTimeout(r, sleep));
	}
}

main();
