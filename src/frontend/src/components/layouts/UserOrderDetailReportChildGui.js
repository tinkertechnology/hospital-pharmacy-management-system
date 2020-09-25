import React, { Component } from "react";

import { Table, Popconfirm, Icon } from "antd";

import { connect } from "react-redux";
import PropTypes from "prop-types";

import {getUserOrderDetailData, getProducts, deleteProduct } from "../../actions/UserOrderDetailReportAction";
import { getCategories } from "../../actions/categories";

import "./product-table.css";

export class UserOrderDetailReportChildGui extends Component {
  state = {
    products: []
  };

  static propTypes = {
    products: PropTypes.array.isRequired,
    getProducts: PropTypes.func.isRequired,
    deleteProduct: PropTypes.func.isRequired,
    getUserOrderDetailData: PropTypes.func.isRequired
  };

  componentDidMount() {
   // this.props.getProducts();
    this.props.getCategories();
    this.props.getUserOrderDetailData();
    
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
        title: "State",
        dataIndex: "state",
        key: "state"
      },
      {
        title: "City",
        dataIndex: "city",
        key: "city"
      },
      {
        title: "Street",
        dataIndex: "street",
        key: "street"
      },
      {
        title: "Product",
        dataIndex: "title",
        key: "title"
      },

      {
        title: "Quantity",
        dataIndex: "quantity",
        key: "quantity",
        //sortDirections: ['descend', 'ascend'],
        sortDirections: ['ascend', 'descend', 'ascend'],
        sorter: {
          compare: (a, b) => a.quantity - b.quantity,
          multiple: 2,
        },
      },
      {
        title: "Ordered at",
        dataIndex: "created_at",
        key: "created_at",
        sorter: (a, b) => new Date(a.created_at) - new Date(b.created_at)
      },
      {
        title: "Latitude",
        dataIndex: "order_latitude",
        key: "order_latitude"
      },
      {
        title: "Longitude",
        dataIndex: "order_longitude",
        key: "order_longitude"
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
    let i=0;
    return (
      <Table
        className="product-table"
        columns={columns}
        dataSource={this.props.products.map(product => ({
          key: product.created_at + product.mobile + i++,
          firstname: product.firstname,
          lastname: product.lastname,
          mobile: product.mobile,
          state: product.state,
          city: product.city,
          street: product.street,
          title: product.title,
          quantity: product.quantity,
          created_at: product.created_at,
          order_latitude: product.order_latitude,
          order_longitude: product.order_longitude
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
  //products: state.products.products,
  categories: state.categories.categories,
  products: state.UserOrderDetailReportReducer.products

});

export default connect(
  mapStateToProps,
  {getUserOrderDetailData, getProducts, getCategories, deleteProduct }
)(UserOrderDetailReportChildGui);
