import mongoose from "mongoose";

const mangaSchema = mongoose.Schema({
  record_id: Number,
  manga_name: String,
  manga_chapters: [String],
  img_link_bg: String,
  chapter_links: [String],
});

const MangaModel = mongoose.model("manga_app_records", mangaSchema);

export default MangaModel;
