import React from "react";
import styles from "./styles.css";

const Post = ({ post }) => {
  const items = [];

  for (var i = 0; i < post.manga_chapters.length; i++) {
    items.push(<a href={post.chapter_links[i]}>{post.manga_chapters[i]}</a>);
  }

  return (
    <>
      <div>
        <h1>{post.manga_name}</h1>
        <img src={post.img_link_bg} alt="{Manga} Background" />
        {items}
      </div>
    </>
  );
};

export default Post;
