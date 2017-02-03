// State argument is not applications state, only the state this reducer is responsible for.
export default function(state = null, action) {
  switch(action.type) {
    case 'METRIC_SELECTED':
      return action.payload
  }

  return state
}
