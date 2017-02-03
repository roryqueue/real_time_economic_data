import { combineReducers } from 'redux'
// import BooksReducer from './reducer_books'
// import ActiveBook from './reducer_active_book'
// import SelectedMetric from './reducer_selected_metric'
// import ReleaseData from './reducer_release_data'


function selectedMetric(state = null, action) {
  switch(action.type) {
    case 'METRIC_SELECTED':
      return action.payload
  }

  return state
}

function releaseData(state = null, action) {
  switch(action.type) {
    case 'RELEASE_DATA_SELECTED':
      return action.payload
  }

  return state
}



const rootReducer = combineReducers({
  // books: BooksReducer,
  // activeBook: ActiveBook,
  selectedMetric: selectedMetric,
  releaseData: releaseData
})

export default rootReducer
