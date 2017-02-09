import React, { Component } from 'react'
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
// class MetricList extends Component {

  // constructor(props) {
  //   super(props);
  //   this.state = {
  //     metrics: []
  //   };
  // }

  // getMetricList() {
  //   const baseApiUrl = 'http://localhost:3333/';
  //   fetch(baseApiUrl)
  //     .then(response => response.json())
  //     .then(response => response.map((metric) => metric.name))
  //     .then(response => this.setState({ metrics: response }));
  // }

  // componentDidMount() {
  //   this.getMetricList();
  // }

//   renderList() {
//     return this.state.metrics.map;
//   }

//   render() {
//     return (

//     )
//   }
// }

export default MetricList
