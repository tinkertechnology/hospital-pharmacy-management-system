import React, { Component } from "react";

import { Layout, Menu, Breadcrumb, Icon, PageHeader } from "antd";
const { Header, Content, Footer, Sider } = Layout;

import SideNav from "../layouts/SideNav";
import UserMenu from "../accounts/UserMenu";

import ReportTable from "../layouts/Reports";

export class Reports extends Component {
  render() {
    return (
      <Layout style={{ minHeight: "100vh" }}>
        <SideNav selected_key="4" submenu_key="sub2" />
        <Layout>
          <Content style={{ margin: "0 16px" }}>
            <UserMenu />
            <div className="container">
              <Breadcrumb style={{ margin: "16px 0" }}>
                <Breadcrumb.Item>Admin</Breadcrumb.Item>
                <Breadcrumb.Item>Store</Breadcrumb.Item>
              </Breadcrumb>
              <hr />
            </div>
            <div
              className="container"
              style={{ padding: 24, background: "#fff", minHeight: 360 }}
            >
              <PageHeader title="Product Report by Users" />
              <div className="container-fluid products">
                <ReportTable />
              </div>
            </div>
          </Content>
          <Footer style={{ textAlign: "center" }}>Copyright 2020</Footer>
        </Layout>
      </Layout>
    );
  }
}

const mapStateToProps = state => ({
  reports: state.reports.reports
  
});

export default Reports;
