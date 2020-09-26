import React, { Component } from "react";

import { Form, Input, Layout, Breadcrumb, Select, Button } from "antd";
const { Content, Footer } = Layout;
const { Option } = Select;

import { connect } from "react-redux";
import PropTypes from "prop-types";

import {sendSms } from "../../actions/sendSmsAction";


import SideNav from "../layouts/SideNav";
import UserMenu from "../accounts/UserMenu";

import "./add_product.css";

export class SMSContainerParentGui extends Component {
  static propTypes = {
    sendSms: PropTypes.func.isRequired
  };

  componentDidMount() {
    // this.props.getCategories();
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
        this.props.sendSms(values);
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
                <Breadcrumb.Item>Send SMS</Breadcrumb.Item>
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
                id="send-sms-form"
              >
                <div className="row">
                  <div className="col-md-6">
                    <Form.Item label="Mobile number">
                      {getFieldDecorator("mobile number", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide Mobile Number"
                          }
                        ]
                      })(<Input name="mobile" required />)}
                    </Form.Item>
                    <Form.Item label="Text SMS">
                      {getFieldDecorator("text-sms", {
                        rules: [
                          {
                            required: false
                          }
                        ]
                      })(<Input type="text-area" name="message" />)}
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
  sendSms: state.sendSms.sendSms
});

export default connect(
  mapStateToProps,
  { sendSms }
)(Form.create({ name: "sendSms" })(SMSContainerParentGui));
