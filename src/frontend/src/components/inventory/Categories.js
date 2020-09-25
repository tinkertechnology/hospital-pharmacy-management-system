import React, { Component } from "react";
import { Layout, Menu, Breadcrumb, Icon } from "antd";
const { Header, Content, Footer, Sider } = Layout;

import { connect } from "react-redux";
import PropTypes from "prop-types";
import { getCategories, deleteCategory } from "../../actions/categories";

import AddCategoryForm from "../layouts/AddCategoryForm";
import SideNav from "../layouts/SideNav";
import UserMenu from "../accounts/UserMenu";

export class Categories extends Component {
  static propTypes = {
    categories: PropTypes.array.isRequired,
    getCategories: PropTypes.func.isRequired,
    deleteCategory: PropTypes.func.isRequired
  };

  componentDidMount() {
    this.props.getCategories();
  }

  render() {
    return (
      <Layout style={{ minHeight: "100vh" }}>
        <SideNav selected_key="6" submenu_key="sub2" />
        <Layout>
          <Content style={{ margin: "0 16px" }}>
            <UserMenu />
            <div className="container">
              <Breadcrumb style={{ margin: "16px 0" }}>
                <Breadcrumb.Item>Admin</Breadcrumb.Item>
                <Breadcrumb.Item>Categories</Breadcrumb.Item>
              </Breadcrumb>
              <hr />
              <div
                className="row"
                style={{ padding: 24, background: "#fff", minHeight: 360 }}
              >
                <AddCategoryForm />
                <table className="table table-striped">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {this.props.categories.map(category => (
                      <tr key={category.id}>
                        <th>{category.category}</th>
                        <td>
                          <button
                            onClick={this.props.deleteCategory.bind(
                              this,
                              category.id
                            )}
                            className="btn btn-danger btn-sm"
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
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
  categories: state.categories.categories
});

export default connect(
  mapStateToProps,
  { getCategories, deleteCategory }
)(Categories);
