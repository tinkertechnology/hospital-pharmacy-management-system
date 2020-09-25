import {GET_getUserOrderDetailData, GET_PRODUCTS, ADD_PRODUCT, DELETE_PRODUCT } from "../actions/types.js";

const initialState = {
  products: []
};
export default function(state = initialState, action) {
  switch (action.type) {
    case GET_getUserOrderDetailData:
      return {
        ...state,
        products: action.payload
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
