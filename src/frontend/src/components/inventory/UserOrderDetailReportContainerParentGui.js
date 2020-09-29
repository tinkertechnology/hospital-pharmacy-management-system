import React, { Component } from 'react';

import { Layout, Menu, Breadcrumb, Icon, PageHeader } from 'antd';
const { Header, Content, Footer, Sider } = Layout;

import SideNav from '../layouts/SideNav';
import UserMenu from '../accounts/UserMenu';

import UserOrderDetailReportChildGui from '../layouts/UserOrderDetailReportChildGui';

export class UserOrderDetailReportContainerParentGui extends Component {
  render() {
    return (
      <Layout style={{ minHeight: '100vh' }}>
        <SideNav selected_key="13" submenu_key="sub2" />
        <Layout>
          <Content style={{ margin: '0 16px' }}>
            <UserMenu />
            <div className="container">
              <Breadcrumb style={{ margin: '16px 0' }}>
                <Breadcrumb.Item>Admin</Breadcrumb.Item>
                <Breadcrumb.Item>Store</Breadcrumb.Item>
              </Breadcrumb>
              <hr />
            </div>
            <div
              className="container"
              style={{ padding: 24, background: '#fff', minHeight: 360 }}
            >
              <PageHeader title="User Detail orders" />
              <div className="container-fluid products">
                <UserOrderDetailReportChildGui />
              </div>
            </div>
          </Content>
          <Footer style={{ textAlign: 'center' }}>Copyright ©2018</Footer>
        </Layout>
      </Layout>
    );
  }
}

const mapStateToProps = (state) => ({
  products: state.products.products,
  categories: state.categories.categories,
});

export default UserOrderDetailReportContainerParentGui;
