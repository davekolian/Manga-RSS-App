import express from "express";

import { getPosts } from "../controller/posts.js";

const router = express.Router();

router.get("/", getPosts);

export default router;
