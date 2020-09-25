import React, { Component } from "react";
import { Form, Input, Icon, Layout, Breadcrumb } from "antd";
const { Content, Footer } = Layout;
import SideNav from "../layouts/SideNav";
import UserMenu from "../accounts/UserMenu";
import SalesTable from "../layouts/SalesTable";

class Sales extends Component {
  state = {};
  render() {
    return (
      <Layout style={{ minHeight: "100vh" }}>
        <SideNav selected_key="9" submenu_key="sub3" />
        <Layout>
          <Content style={{ margin: "0 16px" }}>
            <UserMenu />
            <div className="container">
              <Breadcrumb style={{ margin: "16px 0" }}>
                <Breadcrumb.Item>Admin</Breadcrumb.Item>
                <Breadcrumb.Item>Sales</Breadcrumb.Item>
              </Breadcrumb>
              <hr />
            </div>
            <div
              className="container"
              style={{ padding: 24, background: "#fff", minHeight: 360 }}
            >
              <SalesTable />
            </div>
          </Content>
          <Footer style={{ textAlign: "center" }}>Copyright ©2018</Footer>
        </Layout>
      </Layout>
    );
  }
}

export default Form.create({ name: "sales" })(Sales);
