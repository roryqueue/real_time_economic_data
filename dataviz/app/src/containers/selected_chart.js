import { connect } from 'react-redux'
import {  } from '../actions'
import Chart from '../components/chart'

const defaultData = [
      {name: 'CPI66Q1', uv: 4000, pv: 2400, amt: 2400},
      {name: 'CPI66Q2', uv: 3000, pv: 1398, amt: 2210},
      {name: 'CPI66Q3', uv: 2000, pv: 9800, amt: 2290},
      {name: 'CPI66Q4', uv: 2780, pv: 3908, amt: 2000},
      {name: 'CPI67Q1', uv: 1890, pv: 4800, amt: 2181},
      {name: 'CPI67Q2', uv: 2390, pv: 3800, amt: 2500},
      {name: 'CPI67Q3', uv: 3490, pv: 4300, amt: 2100},
      {name: 'CPI67Q4', uv: 3490, pv: 4300, amt: 2100},
];

const mapStateToProps = (state) => {
  console.log(state)
  let releaseData = defaultData

  if (state.releaseData !== null && state.metric !== null) {
    releaseData = state.releaseData.map(function(releasePeriod) {
      return {
        name: state.metric,
        uv: 0,
        pv: 0,
        amt: parseFloat(releasePeriod.metric_values[0].value)
      }
    })
  }

  return {
    releaseData
  }
}

const mapDispatchToProps = (dispatch) => {
  return {}
}

const SelectedChart = connect(
  mapStateToProps,
  mapDispatchToProps
)(Chart)

export default SelectedChart
