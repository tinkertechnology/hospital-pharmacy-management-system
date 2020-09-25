import React, { Component } from "react";
import { Layout, Menu, Breadcrumb, Icon } from "antd";
const { Header, Content, Footer, Sider } = Layout;

import { loadUser } from "../../actions/auth";

import { connect } from "react-redux";
import PropTypes from "prop-types";

import SideNav from "../layouts/SideNav";
import UserMenu from "../accounts/UserMenu";

export class Dashboard extends Component {
  render() {
    return (
      <Layout style={{ minHeight: "100vh" }}>
        <SideNav selected_key="1" submenu_key="" />
        <Layout>
          <Content style={{ margin: "0 16px" }}>
            <UserMenu />
            <div className="container">
              <Breadcrumb style={{ margin: "16px 0" }}>
                <Breadcrumb.Item>Admin</Breadcrumb.Item>
                <Breadcrumb.Item>Dashboard</Breadcrumb.Item>
              </Breadcrumb>
              <hr />
            </div>
          </Content>
        </Layout>
      </Layout>
    );
  }
}

const mapStateToProps = state => ({
  auth: state.auth
});

export default connect(
  mapStateToProps,
  { loadUser }
)(Dashboard);
