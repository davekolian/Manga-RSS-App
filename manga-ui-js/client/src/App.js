import React, { useEffect } from "react";
import { useDispatch } from "react-redux";

import Posts from "./components/Posts/Posts";

import { getPosts } from "./actions/posts";

const App = () => {
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(getPosts());
  }, [dispatch]);

  return (
    <>
      <Posts />
    </>
  );
};

export default App;
