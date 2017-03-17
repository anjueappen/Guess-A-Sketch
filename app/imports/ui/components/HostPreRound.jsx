import React from 'react';
import { _ } from 'meteor/underscore';
import { Session } from 'meteor/session';

import BaseComponent from './BaseComponent.jsx';
import Prompt from './Prompt.jsx';
import Timer from './Timer.jsx';

import {
  playRound,
} from '/imports/api/methods';


export default class HostPreRound extends BaseComponent {
  constructor(props) {
    super(props);
  }

  onTimeout(room) {
    const didPlayRound = playRound.call({
      room_id: room._id,
    });
    if (!didPlayRound) {
      console.error('Failed to start/play round. Server rejected request.');
      return;
    }
  }

  render() {
    const {
      round,
      room,
    } = this.props;

    return (
      <div className="host-pre-container">
        <h1>Round #{round.index + 1}</h1>
        <div className="host-pre">
          <Prompt prompt={round.prompt} />
          <Timer
            room={room}
            time={3}
            onTimeout={this.onTimeout.bind(null, room)}
            text={'Round starts in '} />
        </div>
      </div>
    );
  }
}

HostPreRound.propTypes = {
  round: React.PropTypes.object,
  room: React.PropTypes.object,
};