import React from "react";
import Post from "./Post/Post";
import { Grid, CircularProgress } from "@material-ui/core";

import { useSelector } from "react-redux";

const Posts = () => {
  const posts = useSelector((state) => state.posts);

  console.log(posts);

  return !posts.length ? (
    <CircularProgress />
  ) : (
    <Grid>
      {posts.map((post) => (
        <Post post={post} />
      ))}
    </Grid>
  );
};

export default Posts;
