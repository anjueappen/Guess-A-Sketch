import React from 'react';
import { Session } from 'meteor/session';
import { _ } from 'meteor/underscore';
import BaseComponent from '../../components/BaseComponent.jsx';

import ParticipantPreGameScreen from '../../components/ParticipantPreGameScreen.jsx';
import ParticipantPlayRound from '../../components/ParticipantPlayRound.jsx';
import ParticipantRoundResults from '../../components/ParticipantRoundResults.jsx';
import ParticipantEndGameScreen from '../../components/ParticipantEndGameScreen.jsx';
import ErrorMessage from '../../components/ErrorMessage.jsx';

import { leaveRoom } from '/imports/api/methods';
import { PLAYER } from '/imports/api/session';

import {
  roundHasCompleted,
  gameHasStarted,
  gameHasEnded,
  currentRound,
  latestCompletedRound
} from '/imports/game-status';


export default class ParticipantGameScreen extends BaseComponent {
  constructor(props) {
    super(props);
    this.state = {
      sketch: null,
    };

    this.latestRoundStatus = currentRound(this.props.room).status;
  }

  componentWillUnmount() {
    // Leave the room.
    const didLeaveRoom = leaveRoom.call({
      room_id: this.props.room._id,
      player: Session.get(PLAYER),
    });
    if (!didLeaveRoom) {
      console.error('Failed to leave room.');
      return;
    }
  }

  componentWillUpdate(nextProps, nextState) {
    if (roundHasCompleted(this.props.room, nextProps.room)) {
      const didSubmitSketch = submitSketch.call({
        player: Session.get(PLAYER),
        sketch: Session.get(SKETCH),
        prompt: latestCompletedRound(this.props.room).prompt,
      });

      if (!didSubmitSketch) {
        console.error('Failed to submit sketch');
        return;
      }
    }
  }

  render() {
    const {
      loading,
      room,
    } = this.props;

    // ---
    // Loading and error handling
    // TODO make these pages pretty.
    // ---
    if (loading) {
      return (
        <p>Loading...</p>
      );
    } else if (!room) {
      // The player navigated directly here without joining a room.
      // Don't allow this!
      console.error('Error: room is undefined.');
      return <ErrorMessage />
    }

    // ---
    // Actual page rendering
    // ---
    if (!gameHasStarted(room)) {
      return <ParticipantPreGameScreen room={room} />;
    } else if (gameHasEnded(room)) {
      return <ParticipantEndGameScreen room={room} />;
    } else {
      const round = currentRound(room);
      if (!round) {
        console.error('Current round is undefined. What the heck! Something is wrong.');
        return <ErrorMessage />
      }

      if (round.status === 'CREATED') {
        // The round has not started yet. We are in-between rounds.
        // So, we want to display results for the *previous* round.
        return <ParticipantRoundResults round={latestCompletedRound(room)} />
      } else if (round.status === 'PLAYING') {
        return <ParticipantPlayRound round={round} />
      } else {
        console.error('Current round is in an illegal state');
        return <ErrorMessage />
      }   
    } 
  }
}

ParticipantGameScreen.propTypes = {
  loading: React.PropTypes.bool,
  room: React.PropTypes.object,
};
