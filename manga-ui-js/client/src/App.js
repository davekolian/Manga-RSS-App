import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import styles from './styles.css';

import { getPosts } from './actions/posts';
import Post from './components/Post/Post';

import { useSelector } from 'react-redux';

import logo from './icons/logo.png';

import github from './icons/github.png';
import instagram from './icons/instagram.png';
import website from './icons/website.png';

const App = () => {
	const dispatch = useDispatch();
	const posts = useSelector((state) => state.posts);

	useEffect(() => {
		dispatch(getPosts());
	}, [dispatch]);

	return (
		<div>
			<div className="header">
				<div className="logo">
					<img src={logo} alt="logo" />
				</div>
				<h1 style={styles.h1}>Manga RSS</h1>
			</div>
			<div className="nav-bar">
				<div className="nav-bar-container">
					<a href="/">Latest</a>
					<a href="/#">Manga List</a>
					<a href="/#" className="search">
						Search
					</a>
				</div>
			</div>
			{!posts.length ? (
				<div className="loader-wrapper">
					<span className="loader"></span>
					<span className="loader-text">Loading... Please wait</span>
				</div>
			) : (
				<div className="container">
					{posts.map((post) => (
						<Post post={post} key={post.record_id} />
					))}
				</div>
			)}

			<div className="footer">
				<div className="images">
					<a
						href="https://github.com/davekolian"
						target="_blank"
						rel="noreferrer"
					>
						<img src={github} alt="Github Link" />
					</a>
					<a
						href="https://www.instagram.com/thekolboy/"
						target="_blank"
						rel="noreferrer"
					>
						<img src={instagram} alt="Instagram Link" />
					</a>
					<a
						href="https://davekolian.github.io/"
						target="_blank"
						rel="noreferrer"
					>
						<img src={website} alt="Personal Website Link" />
					</a>
				</div>
				<p> © davekolian. All rights reserved.</p>
			</div>
		</div>
	);
};

export default App;
