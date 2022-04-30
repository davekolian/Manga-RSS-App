import * as api from '../api';

//Action Creators
export const getPosts = () => async (dispatch) => {
	try {
		const { data } = await api.fetchPosts();
		dispatch({ type: 'FETCH_ALL', payload: data });
	} catch (error) {
		console.log(error.message);
	}
};

export const updatePost = (url, new_chapter) => async (dispatch) => {
	try {
		const post = { url, new_chapter };
		const { data } = await api.updatePost(post);
		dispatch({ type: 'UPDATE_FETCH', payload: data });
	} catch (error) {
		console.log(error.message);
	}
};
