import axios from "axios";
import { createMessage, returnErrors } from "./messages";
import { tokenConfig } from "./auth";

import {
  GET_CATEGORIES,
  DELETE_CATEGORY,
  ADD_CATEGORY,
  GET_ERRORS
} from "./types";

//GET Catgories
export const getCategories = () => (dispatch, getState) => {
  axios
    .get(`/api/category/`, tokenConfig(getState))
    .then(res => {
      dispatch({
        type: GET_CATEGORIES,
        payload: res.data
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};

//Delete Catgories
export const deleteCategory = id => (dispatch, getState) => {
  // Get token from state
  const token = getState().auth.token;

  axios
    .delete(`/api/category/${id}/`, tokenConfig(getState))
    .then(res => {
      dispatch(createMessage({ deleteCategory: "Category Deleted" }));
      dispatch({
        type: DELETE_CATEGORY,
        payload: id
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};

//Add Catgories
export const addCategory = cat => (dispatch, getState) => {
  axios
    .post(`/api/category/`, cat, tokenConfig(getState))
    .then(res => {
      dispatch(createMessage({ addCategory: "Category Added" }));
      dispatch({
        type: ADD_CATEGORY,
        payload: res.data
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};

//Update Catgories
export const updateCategory = id => dispatch => {
  axios
    .put(`/api/category/${id}`)
    .then(res => {
      dispatch({
        type: UPDATE_CATEGORY,
        payload: res.data
      });
    })
    .catch(err => console.log(err));
};
