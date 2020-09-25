import React, { Component, Fragment } from "react";
import ReactDOM from "react-dom";
import { HashRouter as Router, Switch, Route, Link, useHistory  } from "react-router-dom";

import { Layout } from "antd";

import "antd/dist/antd.css";

import { Provider } from "react-redux";
import store from "../store";

import { Provider as AlertProvider } from "react-alert";
import AlertTemplate from "react-alert-template-basic";

import Dashboard from "./inventory/Dashboard";
import Categories from "./inventory/Categories";
import ItemList from "./inventory/ItemList";
import Alert from "./layouts/Alert";
import Login from "./accounts/Login";
import AddProduct from "./inventory/AddProduct";
import Orders from "./inventory/Orders";
import CreateOrder from "./inventory/CreateOrder";
import Invoice from "./inventory/Invoice";
import CreateReceipt from "./inventory/CreateReceipt";

import PrivateRoute from "./common/PrivateRoute";

import { loadUser } from "../actions/auth";
import Sales from "./inventory/Sales";
import CreateSale from "./inventory/CreateSale";

// Reports
import Reports from "./inventory/Reports";
import ReportList from "./inventory/ReportList";
import UserOrderDetailReportContainerParentGui from "./inventory/UserOrderDetailReportContainerParentGui";


// Alert Options
const alertOptions = {
  timeout: 3000,
  position: "top center"
};

export class App extends Component {
  componentDidMount() {
    store.dispatch(loadUser());
  }

  render() {
    return (
      <Provider store={store}>
        <AlertProvider template={AlertTemplate} {...alertOptions}>
          <Router>
            <Fragment>
              <Alert />
              <Switch>
                <PrivateRoute exact path="/dashboard" component={Dashboard} />
                <PrivateRoute exact path="/items/" component={ItemList} />
                <PrivateRoute
                  exact
                  path="/categories/"
                  component={Categories}
                />
                <PrivateRoute
                  exact
                  path="/add-product/"
                  component={AddProduct}
                />
                <PrivateRoute exact path="/orders/" component={Orders} />
                <PrivateRoute
                  exact
                  path="/orders/create-order/"
                  component={CreateOrder}
                />
                <PrivateRoute
                  exact
                  path="/reportlist/"
                  component={ReportList}
                />
                <PrivateRoute
                  exact
                  path="/UserOrderDetailReportContainerParentGui/"
                  component={UserOrderDetailReportContainerParentGui}
                />
                <PrivateRoute exact path="/invoices/" component={Invoice} />
                <PrivateRoute
                  state={this.state}
                  exact
                  path="/receipts/:id"
                  component={CreateReceipt}
                />

                <PrivateRoute exact path="/sales/" component={Sales} />
                <PrivateRoute
                  exact
                  path="/sales/create-sale/"
                  component={CreateSale}
                />
                <Route path="/" component={Login} />
              </Switch>
            </Fragment>
          </Router>
        </AlertProvider>
      </Provider>
    );
  }
}

ReactDOM.render(<App />, document.getElementById("app"));
