import React, { Component } from "react";

import { Layout, Menu, Breadcrumb, Icon } from "antd";
const { Content, Footer } = Layout;

import { connect } from "react-redux";
import PropTypes from "prop-types";

import UserMenu from "../accounts/UserMenu";
import SideNav from "../layouts/SideNav";
import InvoiceTable from "../layouts/InvoiceTable";

import { getInvoices } from "../../actions/invoice";

export class Invoice extends Component {
  static propTypes = {
    invoices: PropTypes.array.isRequired,
    getInvoices: PropTypes.func.isRequired
  };

  render() {
    return (
      <Layout style={{ minHeight: "100vh" }}>
        <SideNav selected_key="3" submenu_key="sub1" />
        <Layout>
          <Content style={{ margin: "0 16px" }}>
            <UserMenu />
            <div className="container">
              <Breadcrumb style={{ margin: "16px 0" }}>
                <Breadcrumb.Item>Admin</Breadcrumb.Item>
                <Breadcrumb.Item>Invoices</Breadcrumb.Item>
              </Breadcrumb>
              <hr />
            </div>
            <div
              className="container"
              style={{ padding: 24, background: "#fff", minHeight: 360 }}
            >
              <InvoiceTable />
            </div>
          </Content>
          <Footer style={{ textAlign: "center" }}>Copyright ©2018</Footer>
        </Layout>
      </Layout>
    );
  }
}

const mapStateToProps = state => ({
  invoices: state.invoices.invoices
});

export default connect(
  mapStateToProps,
  { getInvoices }
)(Invoice);
