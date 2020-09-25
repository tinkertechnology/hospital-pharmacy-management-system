import React, { Component } from "react";

import { Row, Col, Descriptions } from "antd";

import Moment from "react-moment";

import "./receipt.css";

export class SaleReceipt extends Component {
  render() {
    return (
      <div className="receipt">
        <Descriptions>
          <Descriptions.Item label="Name">
            {invoice.order_detail ? invoice.order_detail.customer_name : "NA"}
          </Descriptions.Item>
          <Descriptions.Item label="Telephone">
            {invoice.order_detail
              ? invoice.order_detail.personal_contact
              : "NA"}
          </Descriptions.Item>
          <Descriptions.Item label="Address">
            {invoice.order_detail ? invoice.order_detail.address : "NA"}
          </Descriptions.Item>
        </Descriptions>
        <Row>
          <table className="table table-bordered">
            <tbody>
              <tr>
                <th>Product</th>
                <th>Date</th>
                <th>Amount</th>
              </tr>

              <tr>
                <td>
                  {invoice.order_detail
                    ? invoice.order_detail.product_detail.name
                    : "NA"}
                </td>
                <td>
                  <Moment date={receipt.date_time} format="YYYY/MM/DD" />
                </td>
                <td>{receipt.amount}</td>
              </tr>
            </tbody>
          </table>
          <Col span={8} offset={16}>
            <table className="table">
              <tbody>
                <tr>
                  <th>Total</th>
                  <td>{parseFloat(receipt.amount)}</td>
                </tr>
              </tbody>
            </table>
          </Col>
        </Row>
      </div>
    );
  }
}

export default SaleReceipt;
