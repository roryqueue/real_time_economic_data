import React from 'react'
import { XAxis, LineChart, Tooltip, CartesianGrid, Line } from 'recharts'

const Chart = ({ releaseData }) => (
  <LineChart
    width={1000}
    height={600}
    data={releaseData}
    margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
  >
    <XAxis dataKey='name' />
    <Tooltip />
    <CartesianGrid stroke='#f5f5f5' />
    <Line type='monotone' dataKey='uv' stroke='#ff7300' yAxisId={0} />
    <Line type='monotone' dataKey='pv' stroke='#387908' yAxisId={1} />
  </LineChart>
)

export default Chart
