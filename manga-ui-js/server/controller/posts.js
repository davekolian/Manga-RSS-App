import MangaModel from "../mangaSchema/mangaSchema.js";

import express from "express";

const router = express.Router();

export const getPosts = async (req, res) => {
  try {
    const getManga = await MangaModel.find();
    console.log(getManga);
    res.status(200).json(getManga);
  } catch (error) {
    res.status(404).json({ message: error.message });
  }
};

export const createPost = (req, res) => {
  res.send("Post creation!");
};

export default router;
