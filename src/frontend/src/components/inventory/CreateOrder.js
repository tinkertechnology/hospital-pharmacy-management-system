import React, { Component } from "react";
import { Link } from "react-router-dom";

import {
  Form,
  Input,
  Layout,
  Breadcrumb,
  Select,
  Button,
  PageHeader,
  Icon,
  DatePicker
} from "antd";
const { Content, Footer } = Layout;
const { Option } = Select;

import { connect } from "react-redux";
import PropTypes from "prop-types";

import SideNav from "../layouts/SideNav";
import UserMenu from "../accounts/UserMenu";

import { getProducts } from "../../actions/products";
import { createOrder } from "../../actions/orders";

export class CreateOrder extends Component {
  static propTypes = {
    products: PropTypes.array.isRequired,
    getProducts: PropTypes.func.isRequired,
    createOrder: PropTypes.func.isRequired
  };

  componentDidMount() {
    this.props.getProducts();
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

  handleSelectChange = value => {
    var product = this.props.products.find(product => product.id == value);
    this.props.form.setFieldsValue({
      unit_price: product.unit_price
    });
  };

  handleSubmit = e => {
    e.preventDefault();
    this.props.form.validateFieldsAndScroll((err, fieldsValue) => {
      if (!err) {
        const values = {
          ...fieldsValue,
          delivery_date: fieldsValue["delivery_date"].format("YYYY-MM-DD"),
          personal_contact:
            fieldsValue["primary_prfix"] + fieldsValue["personal_contact"],
          office_contact:
            fieldsValue["secondary_prfix"] + fieldsValue["office_contact"],
          quantity: "sadf"
        };
        this.props.createOrder(values);
        this.props.form.resetFields();
      }
    });
  };
  render() {
    const { getFieldDecorator } = this.props.form;
    const primaryPrifix = getFieldDecorator("primary_prfix", {
      initialValue: "977"
    })(
      <Select style={{ width: 70 }}>
        <Option value="977">977</Option>
      </Select>
    );
    const secondaryPrifix = getFieldDecorator("secondary_prfix", {
      initialValue: "977"
    })(
      <Select style={{ width: 70 }}>
        <Option value="977">977</Option>
      </Select>
    );
    return (
      <Layout style={{ minHeight: "100vh" }}>
        <SideNav selected_key="7" submenu_key="sub3" />
        <Layout>
          <Content style={{ margin: "0 16px" }}>
            <UserMenu />
            <div className="container">
              <Breadcrumb style={{ margin: "16px 0" }}>
                <Breadcrumb.Item>Admin</Breadcrumb.Item>
                <Breadcrumb.Item>Create Order</Breadcrumb.Item>
              </Breadcrumb>
              <hr />
            </div>
            <div
              className="container"
              style={{ padding: 24, background: "#fff", minHeight: 360 }}
            >
              <PageHeader
                title="Create Order"
                extra={[
                  <Link
                    title="Go Back"
                    key="create-order"
                    className="btn btn-primary btn-sm"
                    to="/orders/"
                  >
                    <Icon type="arrow-left" />
                  </Link>
                ]}
              />
              <hr />
              <Form onSubmit={this.handleSubmit} id="add-product-form">
                <div className="row">
                  <div className="col-md-6">
                    <Form.Item label="Customer Name">
                      {getFieldDecorator("customer_name", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide Customer Name"
                          }
                        ]
                      })(<Input name="customer_name" />)}
                    </Form.Item>
                    <Form.Item label="Address">
                      {getFieldDecorator("address", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide address"
                          }
                        ]
                      })(<Input name="address" />)}
                    </Form.Item>
                    <Form.Item label="Product">
                      {getFieldDecorator("product", {
                        rules: [
                          {
                            required: true,
                            message: "Please select Product"
                          }
                        ]
                      })(
                        <Select
                          onChange={this.handleSelectChange}
                          name="product"
                          placeholder="Please select a product"
                        >
                          {this.props.products.map(product => (
                            <Option value={product.id} key={product.id}>
                              {product.name}
                            </Option>
                          ))}
                        </Select>
                      )}
                    </Form.Item>
                    <Form.Item label="Delivery Date">
                      {getFieldDecorator("delivery_date", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide Delivery Date"
                          }
                        ]
                      })(<DatePicker />)}
                    </Form.Item>
                  </div>
                  <div className="col-md-6">
                    <Form.Item label="Personal Number">
                      {getFieldDecorator("personal_contact", {
                        rules: [
                          {
                            required: true,
                            message: "Please input your phone number!"
                          }
                        ]
                      })(
                        <Input
                          addonBefore={primaryPrifix}
                          style={{ width: "100%" }}
                        />
                      )}
                    </Form.Item>
                    <Form.Item label="Secondary Number">
                      {getFieldDecorator("office_contact", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide contact number!"
                          }
                        ]
                      })(
                        <Input
                          addonBefore={secondaryPrifix}
                          style={{ width: "100%" }}
                        />
                      )}
                    </Form.Item>
                    <Form.Item label="Quantity">
                      {getFieldDecorator("quantity", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide quantity"
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
                    <Form.Item label="Unit Price">
                      {getFieldDecorator("unit_price", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide Unit Price"
                          }
                        ],
                        setFieldsValue: 1.0
                      })(
                        <Input
                          type="number"
                          onChange={this.handleNumberChange}
                          name="unit_price"
                          required
                          min={1}
                        />
                      )}
                    </Form.Item>
                    <Form.Item
                      style={{
                        float: "right"
                      }}
                      createOrder
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
        </Layout>
      </Layout>
    );
  }
}

const mapStateToProps = state => ({
  products: state.products.products
});

export default connect(
  mapStateToProps,
  { getProducts, createOrder }
)(Form.create({ name: "create_order" })(CreateOrder));
