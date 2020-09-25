import axios from "axios";

//import { GET_INVOICES, GET_RECEIPT, CREATE_RECEIPT } from "./types";
import { GET_REPORTS} from "./types";
import { createMessage, returnErrors } from "./messages";
import { tokenConfig } from "./auth";

export const getReports = () => (dispatch, getState) => {
  axios
    .get(`/reports/UserCountProductWiseReport/`, tokenConfig(getState))
    .then(res => {
      dispatch({
        type: GET_REPORTS,
        payload: res.data
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};

export const filterInvoices = value => (dispatch, getState) => {
  axios
    .get(`/api/invoices/${value}`, tokenConfig(getState))
    .then(res => {
      dispatch({
        type: GET_INVOICES,
        payload: res.data
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};

export const getReceipts = receipts => (dispatch, getState) => {
  dispatch({
    type: GET_RECEIPT,
    payload: receipts
  });
};

export const createReceipt = (receipt, invoice_id) => (dispatch, getState) => {
  axios
    .post(`api/recipts/${invoice_id}`, receipt, tokenConfig(getState))
    .then(res => {
      dispatch(createMessage({ createReceipt: "Receipt Created" }));
      dispatch(getInvoices());
      dispatch({
        type: CREATE_RECEIPT,
        payload: res.data.receipt
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};
