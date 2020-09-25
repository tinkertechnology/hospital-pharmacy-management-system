import axios from "axios";

import { GET_ITEMS } from "./types";

//GET ITEMS
export const getItems = () => dispatch => {
  axios
    .get(`api/items/`)
    .then(res => {
      dispatch({
        type: GET_ITEMS,
        payload: res.data
      });
    })
    .catch(err => console.log(err));
};
