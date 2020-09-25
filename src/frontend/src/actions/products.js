import axios from "axios";

import { GET_PRODUCTS, ADD_PRODUCT, DELETE_PRODUCT } from "./types";
import { createMessage, returnErrors } from "./messages";
import { tokenConfig } from "./auth";

export const getProducts = () => (dispatch, getState) => {
  axios
    .get(`/reports/UserCountProductWiseReport/`, tokenConfig(getState))
    .then(res => {
      dispatch({
        type: GET_PRODUCTS,
        payload: res.data
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};

export const deleteProduct = id => (dispatch, getState) => {
  axios
    .delete(`api/products/${id}`, tokenConfig(getState))
    .then(res => {
      dispatch(createMessage({ deleteProduct: "Product Deleted" }));
      dispatch({
        type: DELETE_PRODUCT,
        payload: id
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};

export const addProduct = product => (dispatch, getState) => {
  axios
    .post(`api/products/`, product, tokenConfig(getState))
    .then(res => {
      dispatch(createMessage({ addProduct: "Product Added" }));
      dispatch({
        type: ADD_PRODUCT,
        payload: res.data
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};
