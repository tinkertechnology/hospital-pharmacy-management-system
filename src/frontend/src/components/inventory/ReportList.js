import React, { Component } from "react";

import { Layout, Menu, Breadcrumb, Icon, PageHeader } from "antd";
const { Header, Content, Footer, Sider } = Layout;

import SideNav from "../layouts/SideNav";
import UserMenu from "../accounts/UserMenu";

import ReportTable from "../layouts/ReportTable";

export class ReportList extends Component {
  render() {
    return (
      <Layout style={{ minHeight: "100vh" }}>
        <SideNav selected_key="12" submenu_key="sub2" />
        <Layout>
          <Content style={{ margin: "0 16px" }}>
            <UserMenu />
            <div className="container">
              <Breadcrumb style={{ margin: "16px 0" }}>
                <Breadcrumb.Item>Admin</Breadcrumb.Item>
                <Breadcrumb.Item>User Wise Reports</Breadcrumb.Item>
              </Breadcrumb>
              <hr />
            </div>
            <div
              className="container"
              style={{ padding: 24, background: "#fff", minHeight: 360 }}
            >
              <PageHeader title="User Wise Product Reports" />
              <div className="container-fluid products">
                <ReportTable />
              </div>
            </div>
          </Content>
          <Footer style={{ textAlign: "center" }}>Copyright ©2018</Footer>
        </Layout>
      </Layout>
    );
  }
}

const mapStateToProps = state => ({
  products: state.products.products,
  categories: state.categories.categories
});

export default ReportList;
