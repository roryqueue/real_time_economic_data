import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import thunkMiddleware from 'redux-thunk';

import App from './components/app';
import rootReducer from './reducers';

const logger = stor => next => action => {
  console.log('dispatching', action)
  let result = next(action)
  console.log('next state', stor.getState())
  return result
}

let store = createStore(
  rootReducer,
  applyMiddleware(thunkMiddleware, logger)
)

ReactDOM.render(
  <Provider store={store}>
    <App store={store} />
  </Provider>
  , document.querySelector('.container'));