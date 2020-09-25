import React, { Component } from "react";
import {
  PageHeader,
  Icon,
  Table,
  Popconfirm,
  Divider,
  Modal,
  Button
} from "antd";

import { Link } from "react-router-dom";
import { connect } from "react-redux";
import PropTypes from "prop-types";

import { getSales, deleteSale, createSale } from "../../actions/sales";

import "./product-table.css";

class SalesTable extends Component {
  state = {
    loading: false,
    visible: false,
    receipt: "",
    sale: ""
  };

  static propTypes = {
    sales: PropTypes.array.isRequired
  };

  componentDidMount() {
    this.props.getSales();
  }

  constructor(props) {
    super(props);
    this.columns = [
      {
        title: "Product",
        dataIndex: "product",
        key: "product"
      },
      {
        title: "Customer Name",
        dataIndex: "customer_name",
        key: "customer_name"
      },
      {
        title: "Discount",
        dataIndex: "discount",
        key: "discount"
      },
      {
        title: "VAT",
        dataIndex: "vat",
        key: "vat"
      },
      {
        title: "Permanent Address",
        dataIndex: "permanent_address",
        key: "permanent_address"
      },
      {
        title: "Temporary Address",
        dataIndex: "temporary_address",
        key: "temporary_address"
      },
      {
        title: "Phone",
        dataIndex: "phone",
        key: "phone"
      },
      {
        title: "Quantity",
        dataIndex: "quantity",
        key: "quantity"
      },
      {
        title: "Unit price",
        dataIndex: "unit_price",
        key: "unit_price"
      },
      {
        title: "Action",
        dataIndex: "action",
        key: "action",
        width: 100,
        render: (text, record) => (
          <span className="action-utton">
            <Popconfirm
              title="Sure to delete?"
              onConfirm={() => this.props.deleteSale(record.key)}
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
            <Divider type="vertical" />
            <a
              style={{
                color: "green",
                fontSize: "1rem"
              }}
              onClick={() => {
                var sale = this.props.sales.find(sale => sale.id == record.key);
                console.log(sale);
                this.setState({
                  visible: true
                });
              }}
              href="javascript:;"
            >
              <Icon type="eye" />
            </a>
          </span>
        )
      }
    ];
  }

  showModal = () => {
    this.setState({
      visible: true
    });
  };
  handlePrint = () => {
    console.log(this.state.receipt_id, this.state.invoice);
    this.setState({ loading: true });
    document.getElementById("receipt-button").style.display = "none";
    window.print();
    document.getElementById("receipt-button").style.display = "block";
    this.setState({ loading: false });
  };

  handleCancel = () => {
    this.setState({ visible: false });
  };

  render() {
    const columns = this.columns;
    const { visible, loading } = this.state;
    return (
      <div className="sales">
        <Modal
          visible={visible}
          title="Receipt"
          onCancel={this.handleCancel}
          footer={[]}
          closable={false}
          id="receipt-modal"
        >
          <div className="ant-modal-footer" id="receipt-button">
            <Button key="back" onClick={this.handleCancel}>
              Return
            </Button>
            <Button
              key="submit"
              type="primary"
              loading={loading}
              onClick={this.handlePrint}
            >
              Print
            </Button>
          </div>
        </Modal>

        <PageHeader
          title="All Sales"
          extra={[
            <Link
              title="Create Sale"
              key="create-sale"
              className="btn btn-success btn-sm"
              to="/sales/create-sale/"
            >
              <Icon type="plus" />
            </Link>
          ]}
        />

        <Table
          size="middle"
          className="row sales-table"
          columns={columns}
          dataSource={this.props.sales.map(sale => ({
            key: sale.id,
            product: sale.product_detail ? sale.product_detail.name : "NA",
            customer_name: sale.customer_name,
            discount: sale.discount,
            vat: sale.vat,
            permanent_address: sale.permanent_addr,
            temporary_address: sale.temporary_addr,
            phone: sale.phone_no,
            quantity: sale.quantity,
            unit_price: sale.unit_price
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
  sales: state.sales.sales
});

export default connect(
  mapStateToProps,
  { getSales, deleteSale, createSale }
)(SalesTable);
