import React, { Component } from 'react'
import { connect } from 'react-redux'
import { selectMetric, selectReleaseData } from '../actions/index'
import { bindActionCreators } from 'Redux'

class MetricList extends Component {

  constructor(props) {
    super(props);
    this.state = {
      metrics: []
    };
  }

  getMetricList() {
    const baseApiUrl = 'http://localhost:3333/';
    fetch(baseApiUrl)
      .then(response => response.json())
      .then(response => response.map((metric) => metric.name))
      .then(response => this.setState({ metrics: response }));
  }

  componentDidMount() {
    this.getMetricList();
  }

  renderList() {
    return this.state.metrics.map((metric, index) => {
      return (
        <li key={metric}>
          <button onClick={() => this.props.selectMetric(metric)}>
            {metric}
          </button>
        </li>
      )
    });
  }

  render() {
    return (
      <div>
        <h1>{this.props.selectedMetric || 'Nothing'}</h1>
        <ul className="list-group col-sm-4">
          {this.renderList()}
        </ul>
      </div>
    )
  }
}

function mapStateToProps(state) {
  // Whatever is returned will show up as props inside of MetricList
  return {
    metrics: state.metrics,
    selectedMetric: state.selectedMetric
  }
}

// Anything returned from this function will end up as props on MetricList container
function mapDispatchToProps(dispatch) {
  // Whenever selectMetric is called, the result should be passed to all of our reducers
  return bindActionCreators({
    selectMetric: selectMetric,
    selectReleaseData: selectReleaseData
  }, dispatch)
}

// Propmote BookList from a component to a container - it needs to know about this new dispatch method, selectBook. Make it available as a prop.
export default connect(mapStateToProps, mapDispatchToProps)(MetricList)
