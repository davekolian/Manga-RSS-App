//#####################################################################
//#                All rights reserved to davekolian                  #
//#####################################################################

import express from 'express';
import postRoutes from './routes/posts.js';

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/posts', postRoutes);
app.get('/', (req, res) => {
	res.send('Welcome to the Manga-RSS-App Web-Fries');
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () =>
	console.log(`Server Running on Port: http://localhost:${PORT}`)
);
