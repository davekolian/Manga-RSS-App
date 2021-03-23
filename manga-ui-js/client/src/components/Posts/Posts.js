import React from "react";
import Post from "./Post/Post";

import { useSelector } from "react-redux";

const Posts = () => {
  const posts = useSelector((state) => state.posts);

  console.log(posts);

  return !posts.length ? (
    <p>Empty DB! :c</p>
  ) : (
    <>
      {posts.map((post) => (
        <Post post={post} />
      ))}
    </>
  );
};

export default Posts;
