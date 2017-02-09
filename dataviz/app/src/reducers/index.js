import { combineReducers } from 'redux'


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
  selectedMetric: selectedMetric,
  releaseData: releaseData
})

export default rootReducer
