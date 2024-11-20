import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

import postRoutes from './routes/posts.js';

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());

app.use('/posts', postRoutes);
app.get('/', (req, res) => {
	res.send('Hello to Manga-RSS-App Api!');
});

dotenv.config();

const PORT = process.env.PORT || 5000;

app.listen(PORT, () =>
	console.log(`Server Running on Port: http://localhost:${PORT}`)
);
