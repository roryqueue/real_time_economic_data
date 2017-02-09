import React from 'react'
import { selectMetric } from '../actions/index'


const MetricList = ({ metrics, onMetricClick, selectedMetric }) => (
  <div>
    <h1>{selectedMetric || 'Nothing'}</h1>
    <ul className="list-group col-sm-4">
      {metrics.map((metric, index) => 
        <li key={metric}>
          <button onClick={() => onMetricClick(metric)}>
            {metric}
          </button>
        </li>
      )}
    </ul>
  </div>
)

export default MetricList
