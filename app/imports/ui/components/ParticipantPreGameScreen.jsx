import React from 'react';
import { Session } from 'meteor/session';
import { _ } from 'meteor/underscore';

import BaseComponent from './BaseComponent.jsx';
import ErrorMessage from './ErrorMessage.jsx';

import { PLAYER } from '/imports/api/session';

export default class ParticipantPreGameScreen extends BaseComponent {
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  render() {
    const {
      loading,
      room,
    } = this.props;

    if (loading) {
      return (
        <p>Loading...</p>
      );
    } else {
      return (
        <div>
          <p>Your name is { Session.get(PLAYER).name }</p>
          <p>Your color is { Session.get(PLAYER).color }</p>
          <p>You're in room { room.name + ' (' + room._id.substring(0, 4) + ')' }</p>
          <p>...hold your horses though, the game hasn't started yet.</p>
        </div>
      );
    }
  }
}

ParticipantPreGameScreen.propTypes = {
  loading: React.PropTypes.bool,
  room: React.PropTypes.object,
};
