import React, { Component, Fragment } from "react";
import { withAlert } from "react-alert";

import { connect } from "react-redux";
import PropTypes from "prop-types";

export class Alert extends Component {
  static propTypes = {
    error: PropTypes.object.isRequired,
    message: PropTypes.object.isRequired
  };

  componentDidUpdate(prevProps) {
    const { error, alert, message } = this.props;
    if (error != prevProps.error) {
      if (error.msg.category) alert.error("Category is required");
      if (error.msg.detail) alert.error("You are not authorized");
      if (error.msg.username) alert.error("Username is required");
      if (error.msg.password) alert.error("Password was not provided");
      if (error.msg.non_field_errors)
        alert.error(error.msg.non_field_errors.join());
      if (error.msg.quantity) alert.error(error.msg.quantity);
      if(error.msg.phone_no) alert.error(error.msg.phone_no);
    }
    if (message !== prevProps.message) {
      if (message.deleteCategory) alert.success(message.deleteCategory);
      if (message.addCategory) alert.success(message.addCategory);
      if (message.addProduct) alert.success(message.addProduct);
      if (message.deleteProduct) alert.success(message.deleteProduct);

      if (message.deleteOrder) alert.success(message.deleteOrder);
      if (message.createOrder) alert.success(message.createOrder);
      if (message.createReceipt) alert.success(message.createReceipt);
      if (message.receiptError) alert.error(message.receiptError);

      if (message.deleteSale) alert.success(message.deleteSale);
      if (message.createSale) alert.success(message.createSale);
    }
  }

  render() {
    return <Fragment />;
  }
}
const mapStateToProps = state => ({
  error: state.errors,
  message: state.messages
});

export default connect(mapStateToProps)(withAlert()(Alert));
