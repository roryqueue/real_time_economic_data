import { combineReducers } from 'redux'

function metrics(state = [], action) {
  switch(action.type) {
    case 'RECIEVE_METRIC_DATA':
      return action.data
    default:
      return state
  }
}

function selectedMetric(state = null, action) {
  switch(action.type) {
    case 'SELECT_METRIC':
      return action.metric
    default:
      return state
  }
}

function releaseData(state = [], action) {
  switch(action.type) {
    case 'RECIEVE_RELEASE_DATA':
      return action.data
    default:
      return state
  }
}

function error(state = null, action) {
  switch(action.type) {
    case 'RECORD_ERROR':
      return action.error
    default:
      return state
  }
}

const rootReducer = combineReducers({
  metrics,
  selectedMetric,
  releaseData,
  error
})

export default rootReducer
