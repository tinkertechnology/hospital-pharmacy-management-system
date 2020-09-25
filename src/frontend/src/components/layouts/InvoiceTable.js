import React, { Component } from "react";
import { Link } from "react-router-dom";

import { Table, Select, PageHeader, Icon } from "antd";

const { Option } = Select;

import { connect } from "react-redux";
import PropTypes from "prop-types";

import { getInvoices, filterInvoices } from "../../actions/invoice";

import "./product-table.css";

export class InvoiceTable extends Component {
  static propTypes = {
    invoices: PropTypes.array.isRequired,
    getInvoices: PropTypes.func.isRequired
  };

  componentDidMount() {
    this.props.getInvoices();
  }

  constructor(props) {
    super(props);
    this.columns = [
      {
        title: "Invoice No",
        dataIndex: "invoice_no",
        key: "invoice_no"
      },
      {
        title: "Customer",
        dataIndex: "customer",
        key: "customer"
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
        title: "Total",
        dataIndex: "total",
        key: "total"
      },
      {
        title: "Paid",
        dataIndex: "paid",
        key: "paid"
      },
      {
        title: "Delivery Date",
        dataIndex: "delivery_date",
        key: "delivery_date"
      },
      {
        title: "Action",
        dataIndex: "",
        key: "x",
        render: (text, record) => (
          <Link
            style={{
              color: "green",
              fontSize: "1rem"
            }}
            to={`/receipts/${record.key}`}
            title="Create Recipt"
          >
            <Icon type="edit" />
          </Link>
        )
      }
    ];
  }

  onChange = value => {
    this.props.filterInvoices(value);
  };
  render() {
    const columns = this.columns;

    return (
      <div className="invoices">
        <PageHeader
          title="Invoices"
          extra={[
            <Select
              key="select"
              showSearch
              style={{ width: 200 }}
              placeholder="Select a person"
              optionFilterProp="children"
              onChange={this.onChange}
              defaultValue="all"
              filterOption={(input, option) =>
                option.props.children
                  .toLowerCase()
                  .indexOf(input.toLowerCase()) >= 0
              }
            >
              <Option value="due" key="s1">
                Due
              </Option>
              <Option value="paid" key="s2">
                Paid
              </Option>
              <Option value="all" key="s3">
                All
              </Option>
            </Select>
          ]}
        />
        <hr />
        <Table
          className="invoice-table"
          columns={columns}
          dataSource={this.props.invoices.map(invoice => ({
            key: invoice.id,
            invoice_no: invoice.id,
            customer: invoice.order_detail
              ? invoice.order_detail.customer_name
              : "NA",
            contact: invoice.order_detail
              ? invoice.order_detail.personal_contact
              : "NA",
            product: invoice.order_detail
              ? invoice.order_detail.product_detail.name
              : "NA",
            quantity: invoice.order_detail
              ? invoice.order_detail.quantity
              : "NA",
            total: invoice.total,
            paid: invoice.paid,
            delivery_date: invoice.order_detail
              ? invoice.order_detail.delivery_date
              : "NA"
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
  invoices: state.invoices.invoices
});

export default connect(
  mapStateToProps,
  { getInvoices, filterInvoices }
)(InvoiceTable);
