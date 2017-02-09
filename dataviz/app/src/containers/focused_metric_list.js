import { connect } from 'react-redux'
import {  } from '../actions'
import MetricList from '../components/metric_list'

const getVisibleTodos = (todos, filter) => {
  switch (filter) {
    case 'SHOW_ALL':
      return todos
    case 'SHOW_COMPLETED':
      return todos.filter(t => t.completed)
    case 'SHOW_ACTIVE':
      return todos.filter(t => !t.completed)
  }
}

// getMetricList() {
//   const baseApiUrl = 'http://localhost:3333/';
//   fetch(baseApiUrl)
//     .then(response => response.json())
//     .then(response => response.map((metric) => metric.name))
//     .then(response => this.setState({ metrics: response }));
// }


const mapStateToProps = (state) => {
  return {
    metrics: [],
    selectedMetric: null
    // todos: getVisibleTodos(state.todos, state.visibilityFilter)
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    onMetricClick: (name) => {
      dispatch(selectMetric(name))
    }
  }
}


const FocusedMetricList = connect(
  mapStateToProps,
  mapDispatchToProps
)(MetricList)

export default FocusedMetricList
