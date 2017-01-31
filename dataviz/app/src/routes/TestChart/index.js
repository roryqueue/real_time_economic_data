import { injectReducer } from '../../store/reducers'

export default (store) => ({
  path : 'testchart',
  /*  Async getComponent is only invoked when route matches   */
  getComponent (nextState, cb) {
    /*  Webpack - use 'require.ensure' to create a split point
        and embed an async module loader (jsonp) when bundling   */
    require.ensure([], (require) => {
      /*  Webpack - use require callback to define
          dependencies for bundling   */
      const TestChart = require('./containers/TestChartContainer').default
      const MetricSelector = require('./containers/MetricSelectorContainer').default
      const reducer = require('./modules/metricSelector').default

      /*  Add the reducer to the store on key 'counter'  */
      injectReducer(store, { key: 'metricSelector', reducer })

      /*  Return getComponent   */
      cb(null, TestChart)

    /* Webpack named bundle   */
    }, 'metricSelector')
  }
})
