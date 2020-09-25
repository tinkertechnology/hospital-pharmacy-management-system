import React, { Component } from "react";

import { Layout, Menu, Breadcrumb, Icon } from "antd";
const { Content, Footer } = Layout;

import { connect } from "react-redux";
import PropTypes from "prop-types";

import UserMenu from "../accounts/UserMenu";
import SideNav from "../layouts/SideNav";
import OrderTable from "../layouts/OrderTable";

import { getOrders } from "../../actions/orders";

export class Orders extends Component {
  static propTypes = {
    orders: PropTypes.array.isRequired,
    getOrders: PropTypes.func.isRequired
  };

  componentDidMount() {
    this.props.getOrders();
  }

  render() {
    return (
      <Layout style={{ minHeight: "100vh" }}>
        <SideNav selected_key="7" submenu_key="sub3" />
        <Layout>
          <Content style={{ margin: "0 16px" }}>
            <UserMenu />
            <div className="container">
              <Breadcrumb style={{ margin: "16px 0" }}>
                <Breadcrumb.Item>Admin</Breadcrumb.Item>
                <Breadcrumb.Item>Orders</Breadcrumb.Item>
              </Breadcrumb>
              <hr />
            </div>
            <div
              className="container"
              style={{ padding: 24, background: "#fff", minHeight: 360 }}
            >
              <OrderTable />
            </div>
          </Content>
          <Footer style={{ textAlign: "center" }}>Copyright ©2018</Footer>
        </Layout>
      </Layout>
    );
  }
}

const mapStateToProps = state => ({
  orders: state.orders.orders
});

export default connect(
  mapStateToProps,
  { getOrders }
)(Orders);
