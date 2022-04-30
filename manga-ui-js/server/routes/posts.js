import express from 'express';

import { getPosts, updatePost } from '../controller/posts.js';

const router = express.Router();

router.get('/', getPosts);
router.post('/', updatePost);

export default router;
