import React, { Component } from "react";
import { Table, Popconfirm, PageHeader, Icon } from "antd";

import { Link } from "react-router-dom";

import { connect } from "react-redux";
import PropTypes from "prop-types";

import { getOrders, deleteOrder } from "../../actions/orders";

import "./product-table.css";

export class OrderTable extends Component {
  static propTypes = {
    orders: PropTypes.array.isRequired,
    getOrders: PropTypes.func.isRequired,
    deleteOrder: PropTypes.func.isRequired
  };

  componentDidMount() {
    this.props.getOrders();
  }

  constructor(props) {
    super(props);
    this.columns = [
      {
        title: "Customer",
        dataIndex: "customer",
        key: "customer"
      },
      {
        title: "Address",
        dataIndex: "address",
        key: "address"
      },
      {
        title: "Contact",
        dataIndex: "contact",
        key: "contact"
      },
      {
        title: "Product",
        dataIndex: "product",
        key: "product"
      },
      {
        title: "Quantity",
        dataIndex: "quantity",
        key: "quantity"
      },
      {
        title: "Amount",
        dataIndex: "amount",
        key: "amount"
      },
      {
        title: "Delivery Date",
        dataIndex: "delivery_date",
        key: "delivery_date"
      },
      {
        title: "Action",
        dataIndex: "action",
        key: "action",
        width: 360,
        render: (text, record) => (
          <Popconfirm
            title="Sure to delete?"
            onConfirm={() => this.props.deleteOrder(record.key)}
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
      <div className="orders">
        <PageHeader
          title="All Orders"
          extra={[
            <Link
              title="Create Order"
              key="create-order"
              className="btn btn-success btn-sm"
              to="/orders/create-order/"
            >
              <Icon type="plus" />
            </Link>
          ]}
        />
        <hr />
        <Table
          className="order-table"
          columns={columns}
          dataSource={this.props.orders.map(order => ({
            key: order.id,
            customer: order.customer_name,
            address: order.address,
            contact: order.personal_contact,
            product: order.product_detail ? order.product_detail.name : "NA",
            quantity: order.quantity,
            amount: order.unit_price * order.quantity,
            delivery_date: order.delivery_date
          }))}
          pagination={{
            defaultPageSize: 5,
            showSizeChanger: true,
            pageSizeOptions: ["5", "10", "20"]
          }}
        />
      </div>
    );
  }
}

const mapStateToProps = state => ({
  orders: state.orders.orders
});

export default connect(
  mapStateToProps,
  { getOrders, deleteOrder }
)(OrderTable);
