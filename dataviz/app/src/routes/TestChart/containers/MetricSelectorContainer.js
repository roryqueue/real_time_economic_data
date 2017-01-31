import { connect } from 'react-redux'
import { selectMetric, requestMetrics, recieveMetric } from '../modules/metricSelector'

import MetricSelector from '../components/MetricSelector'

const mapDispatchToProps = {
  selectMetric,
  requestMetrics,
  recieveMetric
}

const mapStateToProps = (state) => ({
  metrics : state.metrics,
  selectedMetric: state.selectedMetric
})

export default connect(mapStateToProps, mapDispatchToProps)(MetricSelector)
