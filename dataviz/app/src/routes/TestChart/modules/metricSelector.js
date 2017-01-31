// ------------------------------------
// Constants
// ------------------------------------
export const METRIC_SELECTOR_SELECT = 'METRIC_SELECTOR_SELECT'
export const METRIC_SELECTOR_REQUEST = 'METRIC_SELECTOR_REQUEST'
export const METRIC_SELECTOR_RECIEVE = 'METRIC_SELECTOR_RECIEVE'

// ------------------------------------
// Actions
// ------------------------------------
export function selectMetric (metricName) {
  fetchMetrics()
  return {
    type       : METRIC_SELECTOR_SELECT,
    metricName : metricName
  }
}

export function requestMetrics() {
  return {
    type: REQUEST_METRICS
  }
}

export function receiveMetrics(json) {
  console.log("HERE!!!!!")
  return {
    type: RECEIVE_METRICS,
    metrics: json.map(table => table.name)
  }
}

const baseApiUrl = 'http://localhost:3333/'
export function fetchMetrics () {
  return dispatch => {
    dispatch(requestMetrics())
    return fetch(baseApiUrl)
      .then(response => response.json())
      .then(json => dispatch(receiveMetrics(json)))
  }
}

export const actions = {
  selectMetric
}

// ------------------------------------
// Action Handlers
// ------------------------------------
const ACTION_HANDLERS = {
  [METRIC_SELECTOR_SELECT] : (state, action) => {
    state.selectMetric = action.metricName
    return state
  },
  [METRIC_SELECTOR_REQUEST] : (state, action) => state,
  [METRIC_SELECTOR_RECIEVE] : (state, action) => {
    state.metrics = action.metrics
    return state
  }
}

// ------------------------------------
// Reducer
// ------------------------------------
const initialState = {
  metrics : [],//fetchMetrics(),
  selectedMetric: null
}
export default function metricSelectorReducer (state = initialState, action) {
  const handler = ACTION_HANDLERS[action.type]

  return handler ? handler(state, action) : state
}
