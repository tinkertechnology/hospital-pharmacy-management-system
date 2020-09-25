import React, { Component } from "react";
import { Link } from "react-router-dom";

import { Table, Select, PageHeader, Icon } from "antd";

const { Option } = Select;

import { connect } from "react-redux";
import PropTypes from "prop-types";

// import { getInvoices, filterInvoices } from "../../actions/invoice";

import { getReports } from "../../actions/reports";

import "./product-table.css";


export class ReportTable extends Component {
  static propTypes = {
    reports: PropTypes.array.isRequired,
    getReports: PropTypes.func.isRequired
  };

  componentDidMount() {
    this.props.getReports();
  }

  constructor(props) {
    super(props);
    this.columns = [
      {
        title: "First Name ",
        dataIndex: "firstname",
        key: "lastname"
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
        dataIndex: "product",
        key: "product"
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
          title="UserCountProductWiseReport"
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
          dataSource={this.props.reports.map(report => ({
            key: report.mobile,
            // invoice_no: invoice.id,
            firstname: report.firstname
              ? report.firstname
              : "NA",
            lastname: report.lastname
              ? report.firstname
              : "NA",
            mobile: report.mobile
              ? report.mobile
              : "NA",
            title: report.title
              ? report.title
              : "NA",
            product_quantity: report.product_quantity
            ? report.product_quantity
            : "NA",
            // paid: invoice.paid,
            // delivery_date: invoice.order_detail
            //   ? invoice.order_detail.delivery_date
            //   : "NA"
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
  reports: state.reports.reports
});

export default connect(
  mapStateToProps,
  { getReports}
)(ReportTable);
