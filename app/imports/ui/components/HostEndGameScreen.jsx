import React from 'react';
import BaseComponent from './BaseComponent.jsx';


export default class HostEndGameScreen extends BaseComponent {
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  render() {
    const {
      room,
    } = this.props;

    return (
      <p>This will be the post-game overall scoreboard</p>
    );
  }
}

HostEndGameScreen.propTypes = {
  room: React.PropTypes.object,
};
