import React, { Component } from "react";
import { Avatar, Affix, Menu, Dropdown, Button } from "antd";

import { connect } from "react-redux";
import PropTypes from "prop-types";

import "antd/dist/antd.css";
import "./user_menu.css";
import { logout } from "../../actions/auth";
import { loadUser } from "../../actions/auth";

export class UserMenu extends Component {
  state = {
    top: 10,
    bottom: 10
  };
  static propTypes = {
    auth: PropTypes.object.isRequired
  };

  render() {
    const { isAuthenticated, user } = this.props.auth;
    const menu = (
      <Menu className="user-menu-items">
        <div className="text-center user-name">
          <span className="text-center">
            Hello! {user ? user.username : "user"}
          </span>
        </div>
        <span />
        <Menu.Item>
          <a href="#" onClick={this.props.logout}>
            Log Out
          </a>
        </Menu.Item>
        <Menu.Item>
          <a rel="noopener noreferrer" href="javascript:;">
            Profile
          </a>
        </Menu.Item>
      </Menu>
    );
    return (
      <div>
        <Dropdown overlay={menu} placement="topRight">
          <Affix className="user-menu" offsetBottom={this.state.bottom}>
            <a href="javascript:;">
              <Avatar style={{ backgroundColor: "#87d068" }} icon="user" />
            </a>
          </Affix>
        </Dropdown>
      </div>
    );
  }
}

const mapStateToProps = state => ({
  auth: state.auth
});

export default connect(
  mapStateToProps,
  { logout, loadUser }
)(UserMenu);
