import React from 'react';
import post_css from './post.css';
import { useDispatch } from 'react-redux';
import { updatePost } from '../../actions/posts';

const Post = ({ post }) => {
	const dispatch = useDispatch();

	const handleSubmitUpdateChps = (e, post) => {
		e.preventDefault();

		const url = post.url;
		let chapters = post.chapters.map((x) => Number(x));

		const max = Math.max(...chapters);

		dispatch(updatePost(url, max));
	};

	let len = post.manga_chapters.length - 1;
	const last_new_chapter = (
		<a
			style={post_css.a}
			href={post.chapter_links[len]}
			target="_blank"
			rel="noreferrer"
		>
			Read Chapter {post.manga_chapters[len]}
		</a>
	);

	const chapters = post.manga_chapters.map((x) => Number(x));

	const min = Math.min(...chapters);
	const last_read = post.last_read;

	const btn_svg = (
		<svg
			version="1.0"
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 360.000000 360.000000"
			preserveAspectRatio="xMidYMid meet"
			fill="currentColor"
		>
			<g
				transform="translate(0.000000,360.000000) scale(0.100000,-0.100000)"
				stroke="none"
			>
				<path
					d="M3085 2886 c-447 -188 -854 -497 -1168 -886 -106 -132 -231 -314
   -294 -430 -21 -38 -41 -70 -45 -70 -3 0 -18 21 -33 48 -81 139 -255 361 -373
   474 -102 98 -130 106 -227 59 -139 -67 -224 -226 -167 -312 9 -15 55 -60 102
   -101 135 -119 302 -311 458 -528 58 -82 208 -314 245 -381 l19 -33 57 139
   c273 658 720 1313 1231 1801 87 83 222 201 275 241 39 29 37 29 -80 -21z"
				/>
			</g>
		</svg>
	);

	return last_read < min && len >= 0 ? (
		<div className="manga_whole">
			<img
				src={post.img_link_bg}
				alt={post.manga_name}
				referrerPolicy="no-referrer"
			/>
			<p id="size">{len + 1}</p>
			<div className="box">
				<div className="chaps">
					{last_new_chapter}
					<div className="tooltip">
						<button
							onClick={(e) =>
								handleSubmitUpdateChps(e, {
									url: post.url,
									chapters: post.manga_chapters,
								})
							}
						>
							{btn_svg}
						</button>
						<span className="tooltiptext">Mark all as read</span>
					</div>
				</div>
				<p>{post.manga_name}</p>
			</div>
		</div>
	) : null;
};

export default Post;
