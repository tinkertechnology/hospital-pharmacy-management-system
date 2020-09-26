import axios from "axios";

import { SEND_SMS } from "./types";
import { createMessage, returnErrors } from "./messages";
import { tokenConfig } from "./auth";


export const sendSms = sms => (dispatch, getState) => {
  axios
    .post(`api/send_sms_api/`, product, tokenConfig(getState))
    .then(res => {
      dispatch(createMessage({ sendSms: "SMS SENT" }));
      dispatch({
        type: SEND_SMS,
        payload: res.data
      });
    })
    .catch(err =>
      dispatch(returnErrors(err.response.data, err.response.status))
    );
};
