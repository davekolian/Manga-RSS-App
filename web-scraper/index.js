//#####################################################################
//#                All rights reserved to davekolian                  #
//#####################################################################

const puppeteer = require('puppeteer');
require('dotenv').config();
const mongoose = require('mongoose');
const { MongoClient } = require('mongodb');
const express = require('express');

const app = express();
const PORT = 5000;

const urls = [];
const new_chapters = [];
let record_ids = 0;

async function main_scrapers(urls) {
	let browser = await puppeteer.launch({
		headless: false,
		args: ['--start-maximized'],
		defaultViewport: NaN,
	});

	for (let url of urls) {
		let domain = '';
		let split = url.split('//')[1].split('.');
		if (split[0] == 'www') {
			domain = split[1];
		} else {
			domain = split[0];
		}

		let page = await browser.newPage();

		await page.setRequestInterception(true);
		await page.setDefaultNavigationTimeout(0);

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

		if (domain == 'manhuaplus') await get_from_MP(page, url);
		else if (domain == 'reaperscans') await get_from_Reaper(page, url);
		else if (domain == 'asurascans') await get_from_Asura(page, url);
		else if (domain == 'earlym') await get_from_Early(page, url);

		await page.close();
	}

	await browser.close();
}

async function get_from_MP(page, url) {
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
		let link = x[0].children[0].children[0].dataset.src.slice(0, -12);
		let ext = x[0].children[0].children[0].dataset.src.slice(-4);

		let final_link = link + ext;
		return final_link;
	});

	let arr = await page.evaluate(() => {
		let x = document.getElementsByClassName('wp-manga-chapter');
		console.log(x);
		let arr = [];
		for (let i = 0; i < 10; i++) {
			let chapter = x[i].innerText.split(' ').slice(0, 2).join(' ');
			let date = x[i].innerText.split(' ').slice(2).join(' ');
			arr.push([chapter, date, x[i].children[0].href]);
		}

		return arr;
	});

	for (let chap of arr) {
		let date = chap[1].split(' ')[0];
		let period = chap[1].split(' ')[1];
		let chap_no = chap[0].split(' ')[1];
		if (period == 'day' || period == 'hours' || period == 'hour') {
			if (
				((period == 'hour' || period == 'hours') && date <= 24) ||
				(period == 'day' && date <= 1)
			) {
				local_chapters.push(chap_no);
				local_links.push(chap[2]);
			}
		}
	}
	if (local_chapters.length > 0) {
		new_document = {
			record_id: record_ids,
			manga_name: name,
			manga_chapters: local_chapters,
			img_link_bg: img_link,
			chapter_links: local_links,
		};
		record_ids += 1;
		new_chapters.push(new_document);
	}
}

async function get_from_Reaper(page, url) {
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
		for (let i = 0; i < 10; i++) {
			let chapter = x[i].children[1].children[0].children[0].innerText;
			let date = x[i].children[1].children[0].children[1].innerText;
			let link = x[i].children[1].children[0].href;
			arr.push([chapter, date, link]);
		}

		return arr;
	});

	for (let chap of arr) {
		let date = chap[1].split(' ')[0];
		let period = chap[1].split(' ')[1];
		let chap_no = chap[0].split(' ')[1];
		if (period == 'day' || period == 'hours' || period == 'hour') {
			if (
				((period == 'hour' || period == 'hours') && date <= 24) ||
				(period == 'day' && date <= 1)
			) {
				local_chapters.push(chap_no);
				local_links.push(chap[2]);
			}
		}
	}
	if (local_chapters.length > 0) {
		new_document = {
			record_id: record_ids,
			manga_name: name,
			manga_chapters: local_chapters,
			img_link_bg: img_link,
			chapter_links: local_links,
		};
		record_ids += 1;
		new_chapters.push(new_document);
	}
}

async function get_from_Early(page, url) {
	//Do later
}

async function get_from_Asura(page, url) {
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
		let link = x[0].dataset.src;

		return link;
	});

	let arr = await page.evaluate(() => {
		let x = document.getElementsByClassName('eph-num');
		console.log(x);
		let arr = [];
		for (let i = 0; i < 10; i++) {
			let chapter = x[i].children[0].children[0].innerText;
			let date = x[i].children[0].children[1].innerText;
			let link = x[i].children[0].href;
			arr.push([chapter, date, link]);
		}

		return arr;
	});

	for (let chap of arr) {
		let d = new Date();
		const months = [
			'January',
			'February',
			'March',
			'April',
			'May',
			'June',
			'July',
			'August',
			'September',
			'October',
			'November',
			'December',
		];
		let todays_date =
			months[d.getMonth()] + ' ' + d.getDate() + ', ' + d.getFullYear();
		let yest_date =
			months[d.getMonth()] + ' ' + (d.getDate() - 1) + ', ' + d.getFullYear();
		let chap_no = chap[0].split(' ')[1];

		if (chap[1] == todays_date || chap[1] == yest_date) {
			local_chapters.push(chap_no);
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
		};
		record_ids += 1;
		new_chapters.push(new_document);
	}
}

async function getURLs() {
	const uri = process.env.CONNECTION_URL;
	try {
		mongoose
			.connect(uri, {
				useNewUrlParser: true,
				useUnifiedTopology: true,
			})
			.then(() => {
				let server = app.listen(PORT, () =>
					console.log(`Server Running on Port: ${PORT}`)
				);
				server.close();
			})
			.catch((error) => console.log(`${error} did not connect`));

		const getListOfUrls = mongoose.Schema(
			{
				url: String,
			},
			{ collection: process.env.MANGA_LIST_COL }
		);

		const URLCollector = mongoose.model(
			process.env.MANGA_LIST_COL,
			getListOfUrls
		);
		const getURLs = await URLCollector.find({});

		for (let i of getURLs) {
			urls.push(i.url);
		}
	} catch (e) {
		console.error(e);
	} finally {
		await mongoose.disconnect();
		//await app.disconnect();
		//await app.close();
	}
}

async function pushNewToDB() {
	const uri = process.env.CONNECTION_URL;
	try {
		mongoose
			.connect(uri, {
				useNewUrlParser: true,
				useUnifiedTopology: true,
			})
			.then(() => {
				let server = app.listen(PORT, () =>
					console.log(`Server Running on Port: ${PORT}`)
				);
				server.close();
			})
			.catch((error) => console.log(`${error} did not connect`));

		const getListOfUrls = mongoose.Schema(
			{
				record_id: Number,
				manga_name: String,
				manga_chapters: Array,
				img_link_bg: String,
				chapter_links: Array,
			},
			{ collection: process.env.MANGAS_COL }
		);

		const URLCollector = mongoose.model(process.env.MANGAS_COL, getListOfUrls);
		await URLCollector.deleteMany({});

		await URLCollector.insertMany(new_chapters);
	} catch (e) {
		console.error(e);
	} finally {
		await mongoose.disconnect();
		//await app.disconnect();
		//await app.close();
	}
}

async function main() {
	while (true) {
		record_ids = 0;
		await getURLs();
		await main_scrapers(urls);

		console.log(new_chapters);

		//Push
		pushNewToDB();

		let sleep = 1000 * 60 * 60;
		console.log('Sleep for an hour');
		await new Promise((r) => setTimeout(r, sleep));
	}
}

main();
