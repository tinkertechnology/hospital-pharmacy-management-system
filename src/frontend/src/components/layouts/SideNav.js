import React, { Component } from "react";
import { Link } from "react-router-dom";

import { Layout, Menu, Breadcrumb, Icon } from "antd";
import "antd/dist/antd.css";

const { SubMenu } = Menu;
const { Header, Content, Footer, Sider } = Layout;

export class SideNav extends Component {
  state = {
    collapsed: false,
    selected_key: "1"
  };

  onCollapse = collapsed => {
    this.setState({ collapsed });
  };

  render() {
    return (
      <Sider
        collapsible
        collapsed={this.state.collapsed}
        onCollapse={this.onCollapse}
      >
        <div className="logo" />
        <Menu
          theme="dark"
          defaultSelectedKeys={[this.props.selected_key]}
          defaultOpenKeys={[this.props.submenu_key]}
          mode="inline"
        >
          <Menu.Item key="1">
            <Link to="/">
              <Icon type="pie-chart" />
              <span>Dashboard</span>
            </Link>
          </Menu.Item>
          <SubMenu
            key="sub1"
            aria-expanded="true"
            title={
              <span>
                <Icon type="team" />
                <span>Administration</span>
              </span>
            }
          >
            {/* <Menu.Item key="2">
              <Link to="">Customers</Link>
            </Menu.Item>
            <Menu.Item key="3">
              <Link to="/invoices/">Invoices</Link>
            </Menu.Item> */}
          </SubMenu>
          {/* <SubMenu
            key="sub2"
            aria-expanded="true"
            title={
              <span>
                <Icon type="container" />
                <span>Store</span>
              </span>
            }
          >
            <Menu.Item key="4" to="/items/">
              <Link to="/items/">Products</Link>
            </Menu.Item>
            <Menu.Item key="5">
              <Link to="/add-product/">Add Product</Link>
            </Menu.Item>
            <Menu.Item key="6" to="/items/">
              <Link to="/categories/">Categories</Link>
            </Menu.Item>
          </SubMenu> */}

          {/* <SubMenu
            key="sub3"
            aria-expanded="true"
            title={
              <span>
                <Icon type="credit-card" />
                <span>Business</span>
              </span>
            }
          >
            <Menu.Item key="7">
              <Link to="/orders/">Orders</Link>
            </Menu.Item>
            <Menu.Item key="8">
              <Link to="">Purchase</Link>
            </Menu.Item>
            <Menu.Item key="9">
              <Link to="/sales/">Sales</Link>
            </Menu.Item>
          </SubMenu> */}

          <SubMenu
            key="sub2"
            aria-expanded="true"
            title={
              <span>
                <Icon type="container" />
                <span>Reports</span>
              </span>
            }
          >
            <Menu.Item key="12" to="/items/">
              <Link to="/reportlist/">User Wise Reports</Link>
            </Menu.Item>
            <Menu.Item key="13">
              <Link to="/UserOrderDetailReportContainerParentGui/">User Order details</Link>
            </Menu.Item>
           
          </SubMenu>
        </Menu>
      </Sider>
    );
  }
}

export default SideNav;
