import React, { Component } from 'react';
import FocusedMetricList from '../containers/focused_metric_list'
import Chart from './chart'

export default class App extends Component {
  render() {
    return (
      <div>
        <FocusedMetricList />
        <Chart />
      </div>
    )
  }
}
