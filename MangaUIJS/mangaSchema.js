const mongoose = require("mongoose");

const mangaSchema = new mongoose.Schema({
  record_id: Number,
  manga_name: String,
  manga_chapters: [String],
  img_link_bg: String,
  chapter_links: [String],
});

const mangaModel = mongoose.model("manga_app_records", mangaSchema);

module.exports = mangaModel;
