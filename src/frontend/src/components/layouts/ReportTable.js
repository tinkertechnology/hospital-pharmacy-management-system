import React, { Component } from "react";

import { Table, Popconfirm, Icon } from "antd";

import { connect } from "react-redux";
import PropTypes from "prop-types";

import { getProducts, deleteProduct } from "../../actions/reporttables";
import { getCategories } from "../../actions/categories";

import "./product-table.css";

export class ReportTable extends Component {
  state = {
    products: []
  };

  static propTypes = {
    products: PropTypes.array.isRequired,
    getProducts: PropTypes.func.isRequired,
    deleteProduct: PropTypes.func.isRequired
  };

  componentDidMount() {
    this.props.getCategories();
    this.props.getProducts();
  }

  componentDidUpdate() {
    const { products } = this.props;
  }

  constructor(props) {
    super(props);
    this.columns = [
      {
        title: "First Name ",
        dataIndex: "firstname",
        key: "firstname"
      },
      {
        title: "Last Name",
        dataIndex: "lastname",
        key: "lastname"
      },
      {
        title: "Phone number",
        dataIndex: "mobile",
        key: "mobile"
      },

      {
        title: "Product",
        dataIndex: "title",
        key: "title"
      },
      {
        title: "Quantity",
        dataIndex: "product_quantity",
        key: "product_quantity"
      },
      // {
      //   title: "Action",
      //   dataIndex: "",
      //   key: "action",
      //   render: (text, record) => (
      //     <Popconfirm
      //       title="Sure to delete?"
      //       onConfirm={() => this.props.deleteProduct(record.key)}
      //     >
      //       <a
      //         style={{
      //           color: "red",
      //           fontSize: "1rem"
      //         }}
      //         href="javascript:;"
      //       >
      //         <Icon type="close-square" />
      //       </a>
      //     </Popconfirm>
      //   )
      // }
    ];
  }

  render() {
    const columns = this.columns;

    return (
      <Table
        className="product-table"
        columns={columns}
        dataSource={this.props.products.map(product => ({
          key: product.mobile,
          firstname: product.firstname,
          lastname : product.lastname,
          mobile: product.mobile,
          title: product.title,
          product_quantity : product.product_quantity
          // category: product.category_name.category,
          // supplier: product.supplier,
          // price: product.unit_price,
          // quantity: product.quantity
        }))}
        pagination={{
          defaultPageSize: 10,
          showSizeChanger: true,
          pageSizeOptions: ["5", "10", "20"]
        }}
      />
    );
  }
}

const mapStateToProps = state => ({
  products: state.products.products,
  categories: state.categories.categories
});

export default connect(
  mapStateToProps,
  { getProducts, getCategories, deleteProduct }
)(ReportTable);
