import React from 'react'

export const MetricSelector = (props) => (
  <ul>
    {props.metrics.map((metric) => (
      <li>metric.name</li>
    ))}
  </ul>
)

MetricSelector.propTypes = {
  metrics     : React.PropTypes.array.isRequired,
  selectMetric: React.PropTypes.func.isRequired
}

export default MetricSelector
