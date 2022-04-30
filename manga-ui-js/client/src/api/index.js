import axios from 'axios';

const url = 'https://manga-rss-app.herokuapp.com/posts';

export const fetchPosts = () => axios.get(url);
export const updatePost = (newPost) => axios.post(url, newPost);
