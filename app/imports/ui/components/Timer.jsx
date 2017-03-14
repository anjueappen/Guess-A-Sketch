import React from 'react';
import { _ } from 'meteor/underscore';
import i18n from 'meteor/universe:i18n';
import BaseComponent from './BaseComponent.jsx';

import { TIMER } from '/imports/api/session';
import { currentRound } from '/imports/game-status';

import { 
  changeRoundStatus,
  changeRoomStatus,
} from '/imports/api/methods';

export default class Timer extends BaseComponent {

  constructor(props) {
    super(props);
    Session.set(TIMER, props.time);
  }

  componentDidMount() {
    interval_id = setInterval(() => {
      this.setState(() => {
        Session.set(TIMER, Session.get(TIMER) - 1);
        return {}
      });
    }, 1000);
  }

  shouldComponentUpdate(nextProps) {

    if (Session.get(TIMER) > -1) {
      return true; // keep displaying until time is up
    }

    clearInterval(interval_id);

    if (nextProps.isHost) {
      // This is needed to ensure the Participant UI has enough time
      // to catch up and clear the interval before the host changes the
      // round status. 
      var endTime = new Date().getTime() + 500;
      while (new Date().getTime() < endTime);

      const didChangeRoomStatus = changeRoomStatus.call({
        room_id: nextProps.room._id,
        room_status: "JOINABLE"
      });
      if (!didChangeRoomStatus) {
        console.error('Unable to change room status. Server rejected request.');
        return;
      }

      const didChangeRoundStatus = changeRoundStatus.call({
        room_id: nextProps.room._id,
        round_index: currentRound(nextProps.room).index,
        round_status: "COMPLETE"
      });
      if (!didChangeRoundStatus) {
        console.error('Unable to change round status. Server rejected request.');
        return;
      }
    }

    return false;
  }

  render() {
    const { 
      room,
      time 
    } = this.props;

    return (
      <div className="timer">
        Timer: {Session.get(TIMER)}
      </div>
    );
  }
}

Timer.propTypes = {
  room: React.PropTypes.object,
  time: Number,
  isHost: React.PropTypes.bool,
};
