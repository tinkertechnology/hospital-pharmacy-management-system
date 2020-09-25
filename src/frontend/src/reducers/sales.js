import { GET_SALES, DELETE_SALE, CREATE_SALE } from "../actions/types";

const initialState = {
  sales: [],
  receipts: []
};

export default function(state = initialState, action) {
  switch (action.type) {
    case GET_SALES:
      return {
        ...state,
        sales: action.payload
      };
    case DELETE_SALE:
      return {
        ...state,
        sales: state.sales.filter(sale => sale.id !== action.payload)
      };
    case CREATE_SALE:
      return {
        ...state,
        sales: [...state.sales, action.payload]
      };
    default:
      return state;
  }
}
