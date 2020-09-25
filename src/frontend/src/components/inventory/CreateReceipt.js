import React, { Component } from "react";
import { Link } from "react-router-dom";

import Moment from "react-moment";

import {
  Form,
  Modal,
  Table,
  Input,
  Layout,
  Breadcrumb,
  Select,
  Button,
  PageHeader,
  Icon
} from "antd";
const { Content, Footer } = Layout;
const { Option } = Select;

import { connect } from "react-redux";
import PropTypes from "prop-types";

import UserMenu from "../accounts/UserMenu";
import SideNav from "../layouts/SideNav";
import Receipt from "../layouts/Receipt";

import { getReceipts, createReceipt } from "../../actions/invoice";
import { createMessage } from "../../actions/messages";

export class CreateReceipt extends Component {
  state = {
    loading: false,
    visible: false,
    receipt: "",
    invoice: ""
  };
  constructor(props) {
    super(props);
    this.columns = [
      {
        title: "Receipt No",
        dataIndex: "receipt_no",
        key: "receipt_no"
      },
      {
        title: "Amount",
        dataIndex: "amount",
        key: "amount"
      },
      {
        title: "Date",
        dataIndex: "date",
        key: "date"
      },
      {
        title: "Action",
        dataIndex: "",
        key: "x",
        render: (text, record) => (
          <Button
            style={{
              color: "green",
              fontSize: "1rem"
            }}
            onClick={() => {
              var invoice = this.props.invoices.find(
                invoice => invoice.id == this.props.computedMatch.params.id
              );
              var receipt = this.props.receipts.find(
                receipt => receipt.id == record.key
              );
              this.props.getReceipts(invoice.receipts);
              this.setState({
                visible: true,
                receipt: receipt,
                invoice: invoice
              });
            }}
          >
            <Icon type="printer" />
          </Button>
        )
      }
    ];
  }
  componentDidMount() {
    var invoice = this.props.invoices.find(
      invoice => invoice.id == this.props.computedMatch.params.id
    );
    this.props.getReceipts(invoice.receipts);
  }

  static propTypes = {
    invoices: PropTypes.array.isRequired,
    createReceipt: PropTypes.func.isRequired,
    getReceipts: PropTypes.func.isRequired,
    receipts: PropTypes.array.isRequired
  };

  handleSubmit = e => {
    e.preventDefault();
    var invoice = this.props.invoices.find(
      invoice => invoice.id == this.props.computedMatch.params.id
    );

    this.props.form.validateFieldsAndScroll((err, fieldsValue) => {
      var paid_amount =
        parseFloat(invoice.paid) + parseFloat(fieldsValue["amount"]);
      var due_amount = parseFloat(invoice.total) - parseFloat(invoice.paid);

      if (paid_amount > parseFloat(invoice.total) && due_amount > 0) {
        this.props.createMessage({
          receiptError: `This invoice have only Rs.${due_amount} due`
        });
      } else if (due_amount <= 0) {
        this.props.createMessage({
          receiptError: `The invoice is clear`
        });
        this.props.form.resetFields();
      } else {
        this.props.createReceipt(fieldsValue, invoice.id);
        this.props.form.resetFields();
      }
    });
  };

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
    const { getFieldDecorator } = this.props.form;
    const { visible, loading } = this.state;
    const columns = this.columns;
    return (
      <Layout style={{ minHeight: "100vh" }}>
        <SideNav selected_key="3" submenu_key="sub1" />
        <Layout>
          <Modal
            visible={visible}
            title="Receipt"
            onCancel={this.handleCancel}
            footer={[]}
            closable={false}
            id="receipt-modal"
          >
            <Receipt
              invoice={this.state.invoice}
              receipt={this.state.receipt}
            />
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
          <Content style={{ margin: "0 16px" }}>
            <UserMenu />
            <div className="container">
              <Breadcrumb style={{ margin: "16px 0" }}>
                <Breadcrumb.Item>Admin</Breadcrumb.Item>
                <Breadcrumb.Item>Receipt</Breadcrumb.Item>
              </Breadcrumb>
              <hr />
            </div>
            <div
              className="container"
              style={{ padding: 24, background: "#fff", minHeight: 360 }}
            >
              <PageHeader
                title="Create Recipt"
                extra={[
                  <Link
                    key="1"
                    title="Go Back"
                    key="create-order"
                    className="btn btn-primary btn-sm"
                    to="/invoices/"
                  >
                    <Icon type="arrow-left" />
                  </Link>
                ]}
              />
              <hr />
              <div className="row">
                <div className="container" style={{ padding: 24 }}>
                  <Form
                    layout="inline"
                    onSubmit={this.handleSubmit}
                    id="add-product-form"
                  >
                    <Form.Item>
                      {getFieldDecorator("amount", {
                        rules: [
                          {
                            required: true,
                            message: "Please provide quantity"
                          }
                        ]
                      })(
                        <Input
                          placeholder="Amount"
                          type="number"
                          name="amount"
                          step="0.01"
                          min={1}
                        />
                      )}
                    </Form.Item>
                    <Form.Item>
                      <Button type="primary" htmlType="submit">
                        <Icon type="plus" />
                      </Button>
                    </Form.Item>
                  </Form>
                </div>
              </div>
              <div className="row">
                <div className="container">
                  <h5>All recipts</h5>
                  <Table
                    className="receipt-table"
                    columns={columns}
                    dataSource={this.props.receipts.map(receipt => ({
                      key: receipt.id,
                      receipt_no: receipt.id,
                      amount: receipt.amount,
                      date: (
                        <Moment date={receipt.date_time} format="YYYY/MM/DD" />
                      )
                    }))}
                    pagination={{
                      defaultPageSize: 5,
                      showSizeChanger: true,
                      pageSizeOptions: ["5", "10", "20"]
                    }}
                  />
                </div>
              </div>
            </div>
          </Content>
        </Layout>
      </Layout>
    );
  }
}

const mapStateToProps = state => ({
  receipts: state.invoices.receipts,
  invoices: state.invoices.invoices
});

export default connect(
  mapStateToProps,
  { getReceipts, createMessage, createReceipt }
)(Form.create({ name: "create_receipt" })(CreateReceipt));
