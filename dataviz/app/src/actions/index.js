export function requestMetrics() {
  alert("REQUEST_METRICS")
  return {
    type: 'REQUEST_METRICS'
  }
}

export function receiveMetrics(json) {
  alert("RECIEVE_RELEASE_DATA")
  return {
    type: 'RECIEVE_RELEASE_DATA',
    'metric': metric,
    'data': data
  }
}

export function selectReleaseData(metric) {
  const baseApiUrl = 'http://localhost:3333/';
  return dispatch => {
    dispatch(requestMetrics())
    return fetch(baseApiUrl + metric)
      .then(response => response.json())
      .then(json => dispatch(receiveMetrics(metric, data)))
  }
}

export function selectMetric(metric) {
  selectReleaseData(metric)

  return {
    type: 'METRIC_SELECTED',
    payload: metric
  }
}
