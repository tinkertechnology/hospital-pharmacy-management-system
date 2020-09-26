import {SEND_SMS} from "../actions/types.js";

const initialState = {
  sendSms: []
};
export default function(state = initialState, action) {
  switch (action.type) {
    case SEND_SMS:
      return {
        ...state,
        sendSms: action.payload
      };
    default:
      return state;
  }
}
