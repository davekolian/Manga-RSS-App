import { MongoClient, ServerApiVersion } from 'mongodb';

import express from 'express';
import dotenv from 'dotenv';
dotenv.config();

const router = express.Router();

export const getPosts = async (req, res) => {
	try {
		const uri = process.env.CONNECTION_URL;
		const db = process.env.MANGAS_DB;
		const col = process.env.MANGAS_ALL_COL;

		const client = new MongoClient(uri, {
			useNewUrlParser: true,
			useUnifiedTopology: true,
			serverApi: ServerApiVersion.v1,
		});

		client.connect(async (err) => {
			const collection = client.db(db).collection(col);

			const data = await collection.find({}).toArray();

			res.status(200).json(data);

			client.close();
		});
	} catch (error) {
		res.status(404).json({ message: error.message });
	}
};

export const updatePost = (req, res) => {
	try {
		const uri = process.env.CONNECTION_URL;
		const db = process.env.MANGAS_DB;
		const URL_COL_NAME = process.env.MANGAS_URL_COL;
		const ALL_COL_NAME = process.env.MANGAS_ALL_COL;

		const client = new MongoClient(uri, {
			useNewUrlParser: true,
			useUnifiedTopology: true,
			serverApi: ServerApiVersion.v1,
		});

		client.connect(async (err) => {
			const URL_COL = client.db(db).collection(URL_COL_NAME);

			// Updating the URL COL for the web-scraper
			await URL_COL.updateOne(
				{ url: req.body.url },
				{ $set: { last_read: req.body.new_chapter } }
			);

			// Updating the MANGAS col for the client
			const MANGAS_COL = client.db(db).collection(ALL_COL_NAME);
			await MANGAS_COL.updateOne(
				{ url: req.body.url },
				{ $set: { last_read: req.body.new_chapter } }
			);

			const data = await MANGAS_COL.find({}).toArray();

			res.status(200).json(data);

			client.close();
		});
	} catch (error) {
		res.status(404).json({ message: error.message });
	}
};

export default router;
