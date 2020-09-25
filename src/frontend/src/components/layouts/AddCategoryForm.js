import React, { Component } from "react";

import { Form, Input, Button, Divider, Tag } from "antd";

import { connect } from "react-redux";
import PropTypes from "prop-types";
import { addCategory } from "../../actions/categories";

import "./add_category.css";

export class AddCategoryForm extends Component {
  state = {
    category: "",
    formLayout: "horizontal"
  };

  static propTypes = {
    addCategory: PropTypes.func.isRequired
  };

  onSubmit = e => {
    e.preventDefault();
    const { category } = this.state;
    const cat = { category };
    this.props.addCategory(cat);
    this.setState({
      category: ""
    });
  };
  onChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

  render() {
    const { formLayout } = this.state;
    return (
      <Form onSubmit={this.onSubmit} className="form-inline add-category-form">
        <Form.Item>
          <Input
            name="category"
            onChange={this.onChange}
            placeholder="Add Category"
            value={this.state.category}
          />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" htmlType="submit">
            Add
          </Button>
        </Form.Item>
      </Form>
    );
  }
}

export default connect(
  null,
  { addCategory }
)(AddCategoryForm);
