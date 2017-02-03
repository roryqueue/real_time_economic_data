import React, { Component } from 'react';
import MetricList from './metric_list'
import Chart from './chart'

export default class App extends Component {
  render() {
    return (
      <div>
        <MetricList />
        <Chart />
      </div>
    )
  }
}
