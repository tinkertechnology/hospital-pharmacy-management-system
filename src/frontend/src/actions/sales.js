import axios from "axios";

import { GET_SALES, DELETE_SALE } from "./types";
import { createMessage, returnErrors } from "./messages";
import { tokenConfig } from "./auth";

export const getSales = () => (dispatch, getState) => {
  axios
    .get(`/api/sales/`, tokenConfig(getState))
    .then(res => {
      dispatch({
        type: GET_SALES,
        payload: res.data
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};

export const deleteSale = id => (dispatch, getState) => {
  axios
    .delete(`/api/sales/${id}`, tokenConfig(getState))
    .then(res => {
      dispatch(createMessage({ deleteSale: "Sale Deleted" }));
      dispatch({
        type: DELETE_SALE,
        payload: id
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};

export const createSale = sale => (dispatch, getState) => {
  console.log(sale)
  axios
    .post(`/api/sales/`, sale, tokenConfig(getState))
    .then(res => {
      dispatch(createMessage({ createSale: "Sale Created" }));
      dispatch({
        type: CREATE_SALE,
        payload: res.data.order
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};
