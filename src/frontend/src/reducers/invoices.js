import { GET_INVOICES, GET_RECEIPT, CREATE_RECEIPT } from "../actions/types";

const initialState = {
  invoices: [],
  receipts: []
};

export default function(state = initialState, action) {
  switch (action.type) {
    case GET_INVOICES:
      return {
        ...state,
        invoices: action.payload
      };

    case GET_RECEIPT:
      return {
        ...state,
        receipts: action.payload
      };
    case CREATE_RECEIPT:
      return {
        ...state,
        receipts: [...state.receipts, action.payload]
      };
    default:
      return state;
  }
}
