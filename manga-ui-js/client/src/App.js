import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import styles from "./styles.css";

import { getPosts } from "./actions/posts";
import Post from "./components/Post/Post";

import { useSelector } from "react-redux";

import github from "./icons/github.png";
import instagram from "./icons/instagram.png";
import website from "./icons/website.png";

const App = () => {
  const dispatch = useDispatch();
  const posts = useSelector((state) => state.posts);

  useEffect(() => {
    dispatch(getPosts());
  }, [dispatch]);

  const test = {
    margin: "0 auto",
  };
  return !posts.length ? (
    <p>Empty DB! :c</p>
  ) : (
    <div style={test}>
      <div className="header">
        <h1 style={styles.h1}>Manga-RSS-App</h1>
      </div>
      <div className="container">
        {posts.map((post) => (
          <Post post={post} />
        ))}
      </div>
      <div className="footer">
        <div className="images">
          <a href="https://github.com/davekolian" target="_blank">
            <img src={github} alt="Github Link" />
          </a>
          <a href="https://www.instagram.com/thekolboy/" target="_blank">
            <img src={instagram} alt="Instagram Link" />
          </a>
          <a href="" target="_blank">
            <img src={website} alt="Personal Website Link" />
          </a>
        </div>
        <p>Made by davekolian.</p>
      </div>
    </div>
  );
};

export default App;
