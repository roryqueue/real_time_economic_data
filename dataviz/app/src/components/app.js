import React, { Component } from 'react';
import { connect } from 'react-redux'
import FocusedMetricList from '../containers/focused_metric_list'
import SelectedChart from '../containers/selected_chart'
import { fetchMetrics } from '../actions'

class App extends Component {
  
  constructor(props) {
    super(props)
    // this.handleChange = this.handleChange.bind(this)
  }

  componentDidMount() {
    this.props.store.dispatch(fetchMetrics())
  }

  render() {
    return (
      <div>
        <FocusedMetricList />
        <SelectedChart />
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {}
}

const mapDispatchToProps = (dispatch) => {
  return {
    onMetricClick: (name) => {
      dispatch(selectMetric(name))
    }
  }
}

const WrappedApp = connect(
  mapStateToProps,
  mapDispatchToProps
)(App)

export default WrappedApp