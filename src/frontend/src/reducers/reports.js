//import { GET_PRODUCTS, ADD_PRODUCT, DELETE_PRODUCT } from "../actions/types.js";
import { GET_REPORTS} from "../actions/types.js";
const initialState = {
  reports: []
};
export default function(state = initialState, action) {
  switch (action.type) {
    case GET_REPORTS:
      return {
        ...state,
        reports: action.payload
      };
    case ADD_PRODUCT:
      return {
        ...state,
        products: [...state.products, action.payload]
      };
    case DELETE_PRODUCT:
      return {
        ...state,
        products: state.products.filter(
          product => product.id !== action.payload
        )
      };
    default:
      return state;
  }
}
