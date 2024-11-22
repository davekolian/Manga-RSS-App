import React from 'react';
import ReactDOMClient from 'react-dom/client';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { thunk } from 'redux-thunk';
import reducers from './reducers';
import App from './App';

const store = configureStore({
	reducer: reducers,
	middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(thunk),
});
const container = document.getElementById('root');
const root = ReactDOMClient.createRoot(container);

root.render(
	<Provider store={store}>
		<App tab="app" />
	</Provider>
);
