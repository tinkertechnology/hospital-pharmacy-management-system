import React, { Component } from "react";

import { Table, Popconfirm, Icon } from "antd";

import { connect } from "react-redux";
import PropTypes from "prop-types";

import { getProducts, deleteProduct } from "../../actions/products";
import { getCategories } from "../../actions/categories";

import "./product-table.css";

export class ProductTable extends Component {
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
        title: "Name",
        dataIndex: "name",
        key: "name"
      },
      {
        title: "Category",
        dataIndex: "category",
        key: "category"
      },
      {
        title: "Supplier",
        dataIndex: "supplier",
        key: "supplier"
      },
      {
        title: "Price",
        dataIndex: "price",
        key: "price"
      },
      {
        title: "Quantity",
        dataIndex: "quantity",
        key: "quantity"
      },
      {
        title: "Action",
        dataIndex: "",
        key: "action",
        render: (text, record) => (
          <Popconfirm
            title="Sure to delete?"
            onConfirm={() => this.props.deleteProduct(record.key)}
          >
            <a
              style={{
                color: "red",
                fontSize: "1rem"
              }}
              href="javascript:;"
            >
              <Icon type="close-square" />
            </a>
          </Popconfirm>
        )
      }
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
          name: product.firstname,
          // category: product.category_name.category,
          // supplier: product.supplier,
          // price: product.unit_price,
          // quantity: product.quantity
        }))}
        pagination={{
          defaultPageSize: 5,
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
)(ProductTable);
