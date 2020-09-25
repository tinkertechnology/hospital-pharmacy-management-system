import React, { Component } from "react";
import { Link } from "react-router-dom";

import {
  Layout,
  Breadcrumb,
  PageHeader,
  Icon,
  Form,
  Input,
  Select,
  Button
} from "antd";
const { Content, Footer } = Layout;
const { Option } = Select;

import SideNav from "../layouts/SideNav";
import { UserMenu } from "../accounts/UserMenu";

import PropTypes from "prop-types";
import { connect } from "react-redux";

import { createSale } from "../../actions/sales";
import { getProducts } from "../../actions/products";

class CreateSale extends Component {
  static propTypes = {
    products: PropTypes.array.isRequired,
    getProducts: PropTypes.func.isRequired,
    createSale: PropTypes.func.isRequired
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
          phone_no: fieldsValue["primary_prfix"] + fieldsValue["phone_no"]
        };
        console.log("formvalues",values);
        this.props.createSale(values);
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

    return (
      <Layout style={{ minHeight: "100vh" }}>
        <SideNav selected_key="9" submenu_key="sub3" />
        <Layout>
          <Content style={{ margin: "0 16px" }}>
            {/* <UserMenu /> */}
            <div className="container">
              <Breadcrumb style={{ margin: "16px 0" }}>
                <Breadcrumb.Item>Admin</Breadcrumb.Item>
                <Breadcrumb.Item>Create Sale</Breadcrumb.Item>
              </Breadcrumb>
              <hr />
            </div>
            <div
              className="container"
              style={{ padding: 24, background: "#fff", minHeight: 360 }}
            >
              <PageHeader
                title="Create Sale"
                extra={[
                  <Link
                    title="Go Back"
                    key="create-sale"
                    className="btn btn-primary btn-sm"
                    to="/sales/"
                  >
                    <Icon type="arrow-left" />
                  </Link>
                ]}
              />
              <hr />

              <Form onSubmit={this.handleSubmit} id="add-product-form">
                <div className="row">
                  <div className="col-md-6">
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

                    <Form.Item label="Discount">
                      {getFieldDecorator("discount", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide discount"
                          }
                        ],
                        setFieldsValue: 1.0
                      })(
                        <Input
                          type="number"
                          onChange={this.handleNumberChange}
                          name="discount"
                          required
                          min={1}
                        />
                      )}
                    </Form.Item>

                    <Form.Item label="VAT">
                      {getFieldDecorator("vat", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide VAT"
                          }
                        ],
                        setFieldsValue: 1.0
                      })(
                        <Input
                          type="number"
                          onChange={this.handleNumberChange}
                          name="vat"
                          required
                          min={1}
                        />
                      )}
                    </Form.Item>

                    <Form.Item label="Permanent Address">
                      {getFieldDecorator("permanent_addr", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide permanent address"
                          }
                        ]
                      })(<Input name="permanent_addr" />)}
                    </Form.Item>
                  </div>

                  <div className="col-md-6">
                    <Form.Item label="Temporary Address">
                      {getFieldDecorator("temporary_addr", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide temporary address"
                          }
                        ]
                      })(<Input name="temporary_addr" />)}
                    </Form.Item>
                    <Form.Item label="Phone">
                      {getFieldDecorator("phone_no", {
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
                    <br /> <br />
                    <Form.Item
                      style={{
                        float: "right"
                      }}
                      createSale
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
  { getProducts, createSale }
)(Form.create({ name: "create_sale" })(CreateSale));
