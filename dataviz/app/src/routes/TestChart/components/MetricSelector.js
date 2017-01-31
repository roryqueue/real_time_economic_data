import React from 'react'

export const MetricSelector = (props) => (
  <div>
    <h1>{props.selectedMetric}</h1>
    <ul>
      {props.metrics.map((metric) => (
        <button
          className='btn btn-default'
          onClick={props.selectMetric(metric.name)}
        >
          {metric.name}
        </button>
      ))}
    </ul>
  </div>
)

MetricSelector.propTypes = {
  metrics       : React.PropTypes.array.isRequired,
  selectMetric  : React.PropTypes.func.isRequired,
  selectedMetric: React.PropTypes.string
}

export default MetricSelector
