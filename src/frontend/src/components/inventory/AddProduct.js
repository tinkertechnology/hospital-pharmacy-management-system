import React, { Component } from "react";

import { Form, Input, Layout, Breadcrumb, Select, Button } from "antd";
const { Content, Footer } = Layout;
const { Option } = Select;

import { connect } from "react-redux";
import PropTypes from "prop-types";

import { getProducts, addProduct } from "../../actions/products";
import { getCategories } from "../../actions/categories";

import SideNav from "../layouts/SideNav";
import UserMenu from "../accounts/UserMenu";

import "./add_product.css";

export class AddProduct extends Component {
  static propTypes = {
    categories: PropTypes.array.isRequired,
    getCategories: PropTypes.func.isRequired,
    addProduct: PropTypes.func.isRequired
  };

  componentDidMount() {
    this.props.getCategories();
  }

  handleNumberChange = e => {
    const number = parseInt(e.target.value || 0, 10);
    // if (Number.isNaN(number)) {
    //   return;
    // }
    // if (!("value" in this.props)) {
    //   this.setState({ number });
    // }
    // this.triggerChange({ number });
  };

  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFieldsAndScroll((err, values) => {
      if (!err) {
        console.log("Received values of form: ", values);
        this.props.addProduct(values);
        this.props.form.resetFields();
      }
    });
  };

  render() {
    const { getFieldDecorator } = this.props.form;
    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 8 }
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 16 }
      }
    };
    const tailFormItemLayout = {
      wrapperCol: {
        xs: {
          span: 24,
          offset: 0
        },
        sm: {
          span: 16,
          offset: 8
        }
      }
    };
    return (
      <Layout style={{ minHeight: "100vh" }}>
        <SideNav selected_key="5" submenu_key="sub2" />
        <Layout>
          <Content style={{ margin: "0 16px" }}>
            <UserMenu />
            <div className="container">
              <Breadcrumb style={{ margin: "16px 0" }}>
                <Breadcrumb.Item>Admin</Breadcrumb.Item>
                <Breadcrumb.Item>Add Product</Breadcrumb.Item>
              </Breadcrumb>
              <hr />
            </div>
            <div
              className="container"
              style={{ padding: 24, background: "#fff", minHeight: 360 }}
            >
              <Form
                {...formItemLayout}
                onSubmit={this.handleSubmit}
                id="add-product-form"
              >
                <div className="row">
                  <div className="col-md-6">
                    <Form.Item label="Name">
                      {getFieldDecorator("name", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide Name"
                          }
                        ]
                      })(<Input name="name" required />)}
                    </Form.Item>
                    <Form.Item label="Supplier">
                      {getFieldDecorator("supplier", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide Supplier"
                          }
                        ]
                      })(<Input name="supplier" required />)}
                    </Form.Item>
                    <Form.Item label="Category">
                      {getFieldDecorator("category", {
                        rules: [
                          {
                            required: true,
                            message: "Please select Category"
                          }
                        ]
                      })(
                        <Select name="category" required>
                          {this.props.categories.map(category => (
                            <Option value={category.id} key={category.id}>
                              {category.category}
                            </Option>
                          ))}
                        </Select>
                      )}
                    </Form.Item>
                  </div>
                  <div className="col-md-6">
                    <Form.Item label="Price/Unit">
                      {getFieldDecorator("unit_price", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide Unit Price"
                          }
                        ]
                      })(
                        <Input
                          type="number"
                          onChange={this.handleNumberChange}
                          name="unit_price"
                          min={1}
                          required
                        />
                      )}
                    </Form.Item>
                    <Form.Item label="Quantity">
                      {getFieldDecorator("quantity", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide Unit Price"
                          }
                        ]
                      })(
                        <Input
                          type="number"
                          onChange={this.handleNumberChange}
                          name="quantity"
                          required
                          min={1}
                        />
                      )}
                    </Form.Item>
                    <Form.Item label="Description">
                      {getFieldDecorator("description", {
                        rules: [
                          {
                            required: false
                          }
                        ]
                      })(<Input type="text-area" name="description" />)}
                    </Form.Item>
                    <Form.Item
                      style={{
                        float: "right"
                      }}
                    >
                      <Button type="primary" htmlType="submit">
                        Submit
                      </Button>
                    </Form.Item>
                  </div>
                </div>
              </Form>
            </div>
          </Content>
          <Footer style={{ textAlign: "center" }}>Copyright ©2018</Footer>
        </Layout>
      </Layout>
    );
  }
}

// const Wrapped= Form.create({ name: 'register' })(RegistrationForm);
const mapStateToProps = state => ({
  categories: state.categories.categories
});

export default connect(
  mapStateToProps,
  { getCategories, addProduct }
)(Form.create({ name: "add_product" })(AddProduct));
