import axios from "axios";

import { GET_ORDERS, DELETE_ORDER, CREATE_ORDER } from "./types";
import { createMessage, returnErrors } from "./messages";
import { tokenConfig } from "./auth";

export const getOrders = () => (dispatch, getState) => {
  axios
    .get(`/api/orders/`, tokenConfig(getState))
    .then(res => {
      dispatch({
        type: GET_ORDERS,
        payload: res.data
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};

export const deleteOrder = id => (dispatch, getState) => {
  axios
    .delete(`/api/orders/${id}`, tokenConfig(getState))
    .then(res => {
      dispatch(createMessage({ deleteOrder: "Order Deleted" }));
      dispatch({
        type: DELETE_ORDER,
        payload: id
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};

export const createOrder = order => (dispatch, getState) => {
  axios
    .post(`api/orders/`, order, tokenConfig(getState))
    .then(res => {
      dispatch(createMessage({ createOrder: "Order Created" }));
      dispatch({
        type: CREATE_ORDER,
        payload: res.data.order
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};
