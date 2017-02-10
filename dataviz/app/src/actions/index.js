const baseApiUrl = 'http://localhost:3333/';

export function recordError(error) {
  return {
    type: 'RECORD_ERROR',
    error: error
  }
}

export function receiveMetricData(data) {
  return {
    type: 'RECIEVE_METRIC_DATA',
    'data': data
  }
}

export function receiveReleaseData(metric, data) {
  return {
    type: 'RECIEVE_RELEASE_DATA',
    'metric': metric,
    'data': data
  }
}

export function fetchMetrics() {
  return dispatch => {
    return fetch(baseApiUrl)
      .then(response => response.json())
      .then(json => json.map(row => row.name))
      .then(data => dispatch(receiveMetricData(data)))
      .catch(error => dispatch(recordError(error)));
  }
}

export function fetchReleaseData(metric) {
  return dispatch => {
    return fetch(baseApiUrl + metric)
      .then(response => response.json())
      .then(data => dispatch(receiveReleaseData(metric, data)))
      .catch(error => dispatch(recordError(error)));
  }
}

export function selectMetric(metric) {
  return {
    type: 'SELECT_METRIC',
    metric: metric
  }
}
