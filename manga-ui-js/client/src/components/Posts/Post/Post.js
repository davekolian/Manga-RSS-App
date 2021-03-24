import React from "react";
import styles from "./styles.css";

const Post = ({ post }) => {
  const items = [];

  const mainDivStyle = {
    position: "relative",
    margin: "10px",
    width: "225px",
    height: "337px",
    backgroundImage: `url(${post.img_link_bg})`,
    backgroundRepeat: "no-repeat",
    backgroundSize: "cover",
    display: "inline-block",
  };

  for (var i = 0; i < post.manga_chapters.length; i++) {
    items.push(
      <a style={styles.a} href={post.chapter_links[i]}>
        {post.manga_chapters[i]}
      </a>
    );
  }

  return (
    <>
      <div class="main" style={mainDivStyle}>
        <p style={styles.p}>{post.manga_name}</p>
        <div class="chaps">{items}</div>
      </div>
    </>
  );
};

export default Post;
