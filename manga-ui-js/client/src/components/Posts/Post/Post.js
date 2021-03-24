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

  let chapSize = String(post.manga_chapters[0]);

  let gridSize = 0;

  if (chapSize.length === 2) {
    gridSize = 5;
  } else if (chapSize.length === 3) {
    gridSize = 4;
  } else {
    gridSize = 3;
  }

  let gridDivStyle = {
    display: "grid",
    gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
    alignItems: "center",
  };

  for (var i = post.manga_chapters.length - 1; i >= 0; i--) {
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
        <div class="chaps">
          <div style={gridDivStyle}>{items}</div>
        </div>
      </div>
    </>
  );
};

export default Post;
