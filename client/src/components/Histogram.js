import Histogram from 'react-chart-histogram';
import * as React from 'react';

export default function Histogram1 (props) {
  const options = { fillColor: '#02A684', strokeColor: 'black' };

  return (
    <div>
      <h1>{props.title}</h1>
      <Histogram
          xLabels={Object.keys(props.data)}
          yValues={Object.values(props.data)}
          width='1400'
          height='600'
          options={options}
      />
    </div>
  )
};