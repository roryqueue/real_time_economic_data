import { combineReducers } from 'redux'

function metrics(state = [], action) {
  switch(action.type) {
    case 'FETCH_METRICS':
      return action.payload
  }

  return state
}

function selectedMetric(state = null, action) {
  switch(action.type) {
    case 'METRIC_SELECTED':
      return action.payload
  }

  return state
}

function releaseData(state = [], action) {
  switch(action.type) {
    case 'RELEASE_DATA_SELECTED':
      return action.payload
  }

  return state
}



const rootReducer = combineReducers({
  metrics,
  selectedMetric,
  releaseData
})

export default rootReducer
