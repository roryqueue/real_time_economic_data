import React, {Component} from 'react'
import { connect } from 'react-redux'
import { XAxis, LineChart, Tooltip, CartesianGrid, Line } from 'recharts'


class Chart extends Component {
  getReleaseData(metric) {
    const baseApiUrl = 'http://localhost:3333/' + metric;
    fetch(baseApiUrl)
      .then(response => response.json())
      .then(response => response.map((metric) => metric.name))
      .then(response => this.setState({ releaseData: response }));
  }

  render() {
    if (!this.props.releaseData) return <div>Select a metric to get started</div>

    return (
    <LineChart
      width={1000}
      height={600}
      data={defaultData}
      margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
    >
      <XAxis dataKey='name' />
      <Tooltip />
      <CartesianGrid stroke='#f5f5f5' />
      <Line type='monotone' dataKey='uv' stroke='#ff7300' yAxisId={0} />
      <Line type='monotone' dataKey='pv' stroke='#387908' yAxisId={1} />
    </LineChart>
    )
  }
}

function mapStateToProps(state) {
  return {
    selectedMetric: state.selectedMetric,
    releaseData: state.releaseData
  }
}

export default connect(mapStateToProps)(Chart)
