import { combineReducers } from "redux";

import items from "./items";
import errors from "./errors";
import categories from "./categories";
import messages from "./messages";
import auth from "./auth";
import products from "./products";
import orders from "./orders.js";
import invoices from "./invoices.js";
import sales from "./sales.js";
import UserOrderDetailReportReducer from "./UserOrderDetailReportReducer";

export default combineReducers({
  items,
  errors,
  categories,
  messages,
  auth,
  products,
  orders,
  invoices,
  sales,
  UserOrderDetailReportReducer
});
