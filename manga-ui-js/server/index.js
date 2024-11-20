import express from 'express';
import postRoutes from './routes/posts.js';

const app = express();
app.use(function (req, res, next) {
	const allowedOrigins = [
		'http://localhost:5000',
		'http://localhost:3000',
		'https://manga-rss-app.netlify.app/',
	];
	const origin = req.headers.origin;
	if (allowedOrigins.includes(origin)) {
		res.setHeader('Access-Control-Allow-Origin', origin);
	}
	res.header(
		'Access-Control-Allow-Headers',
		'Origin, X-Requested-With, Content-Type, Accept, Authorization'
	);
	res.header('Access-Control-Allow-credentials', true);
	res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, UPDATE');
	next();
});

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/posts', postRoutes);
app.get('/', (req, res) => {
	res.send('Hello to Manga-RSS-App Api!');
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () =>
	console.log(`Server Running on Port: http://localhost:${PORT}`)
);
