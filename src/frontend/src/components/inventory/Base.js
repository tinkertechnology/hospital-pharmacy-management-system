import React, { Component } from "react";
import { HashRouter as Router, Switch, Route, Link } from "react-router-dom";

import SideNav from "./layouts/SideNav";
import { Layout, Menu, Breadcrumb, Icon } from "antd";

import "antd/dist/antd.css";

import SideNav from "./layouts/SideNav";
import Dashboard from "./inventory/Dashboard";
import Categories from "./inventory/Categories";
import ItemList from "./inventory/ItemList";

export class Base extends Component {
  render() {
    return (
      <Layout style={{ minHeight: "100vh" }}>
        <SideNav />
        <Layout>
          <Footer style={{ textAlign: "center" }}>Copyright ©2018</Footer>
        </Layout>
      </Layout>
    );
  }
}

export default Base;
