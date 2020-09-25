import axios from "axios";
import { returnErrors } from "./messages";

import {
  USER_LOADED,
  USER_LOADING,
  AUTH_ERROR,
  LOGIN_FAIL,
  LOGIN_SUCCESS,
  LOGOUT_SUCCESS
} from "./types";

// Check Token and Load User
export const loadUser = () => (dispatch, getState) => {
  // Get token from state
  const token = getState().auth.token;
 console.log(token);
  //Header
  const config = {
    headers: {
      "Content-Type": "application/json"
    }
  };

  if (token) {
    config.headers["Authorization"] = `JWT ${token}`;
    // User Loading
    // dispatch({ type: USER_LOADING });
    axios
      .get("/api/CheckTokenAPIView/", config)
      .then(res => {
        dispatch({
          type: USER_LOADED,
          payload: res.data
        });
      })
      .catch(err => {
        dispatch(returnErrors(err.response.data, err.response.status));
        dispatch({
          type: AUTH_ERROR
        });
      });
  } else {
    dispatch({
      type: AUTH_ERROR
    });
  }
};

// Login User
export const login = (mobile, password) => dispatch => {
  //Header
  var auth_url = '/api/auth/token/';
  const config = {
    headers: {
      "Content-Type": "application/json"
    }
  };
  // Request Body
  const body = JSON.stringify({ mobile, password });
  dispatch({ type: USER_LOADING });
  axios
    .post(auth_url, body, config)
    .then(res => {
      dispatch({
        type: LOGIN_SUCCESS,
        payload: res.data
      });
    })
    .catch(err => {
      dispatch(returnErrors(err.response.data, err.response.status));
      dispatch({
        type: LOGIN_FAIL
      });
    });
};

// LOGOUT USER
export const logout = () => (dispatch, getState) => {
  const config = {
    headers: {
      "Content-Type": "application/json"
    }
  };

  // Get token from state
  const token = getState().auth.token;
  if (token) {
    config.headers["Authorization"] = `JWT ${token}`;
    axios
      //.post("/api/auth/logout/", null, config)
      .get("/api/CheckTokenAPIView/", config)
      .then(res => {
        dispatch({
          type: LOGOUT_SUCCESS
        });
      })
      .catch(err => {
        dispatch(returnErrors(err.response.data, err.response.status));
      });
  }

};

// Setup config with token - helper function
export const tokenConfig = getState => {
  // Get token from state
  const token = getState().auth.token;

  //Header
  const config = {
    headers: {
      "Content-Type": "application/json"
    }
  };
  //If token add token to header
  if (token) {
    config.headers["Authorization"] = `JWT ${token}`;
  }
  return config;
};
