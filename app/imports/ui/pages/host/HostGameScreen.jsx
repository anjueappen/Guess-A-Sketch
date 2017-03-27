import React from 'react';
import { _ } from 'underscore';
import { browserHistory } from 'react-router';

import { Session } from 'meteor/session';
import { HOST_ROOM } from '/imports/api/session';

import { Sketches } from '/imports/api/collections/sketches';
import { Rooms } from '/imports/api/collections/rooms';

import {
  startRound,
  playRound,
  roundTimerOver,
  endRound,
  endGame,
  errors,
} from '/imports/api/methods';
import { 
  getRoundScore,
  getGameScore,
} from '/imports/scoring';
import {
  isPreGame,
  isPostGame,
  isInGame,
  currentRound,
  isLastRound,
} from '/imports/game-status';

import BaseComponent from '../../components/BaseComponent.jsx';
import ErrorMessage from '../../components/ErrorMessage.jsx';

import HostPreGameScreen from '../../components/HostPreGameScreen.jsx';
import HostPreRound from '../../components/HostPreRound.jsx';
import HostPlayRound from '../../components/HostPlayRound.jsx';
import HostRoundResults from '../../components/HostRoundResults.jsx';
import HostEndGameScreen from '../../components/HostEndGameScreen.jsx';


export default class HostGameScreen extends BaseComponent {
  constructor(props) {
    super(props);
  }

  onStartGame(room) {
    console.log(`onStartGame`);
    console.log(room);
    startRound.call({
      room_id: room._id,
    }, (error, result) => {
      if (error) {
        console.error(error, room);
        switch (error.error) {
          case errors.startRound.noRoom:
            alert('The room no longer exists');
            break;
          case errors.startRound.roomStatus:
            alert('Failed to set the room status to playing');
            break;
          case errors.startRound.roundStatus:
            alert('Failed to start the round');
            break;
          case errors.ValidationError:
            alert('ValidationError, check console for args.');
            console.error(room);
            break;
        }
      } else {
        console.log('started game successfully!');
        console.log(Rooms.findOne(room._id));
      }
    });
  }

  onPlayRound(room) {
    playRound.call({
      room_id: room._id,
    }, (error, result) => {
      if (error) {
        switch (error.error) {
          case errors.playRound.noRoom:
            alert('The room no longer exists');
            break;
          case errors.playRound.roundStatus:
            alert('Failed to start the round');
            break;
          default:
            alert(`Unknown playRound error: ${error.error}`);
        }
      }
    });
  }

  onRoundTimerOver(room) {
    roundTimerOver.call({
      room_id: room._id,
    }, (error, result) => {
      if (error) {
        switch (error.error) {
          case errors.roundTimerOver.noRoom:
            alert('The room no longer exists');
            break;
          case errors.roundTimerOver.roomStatus:
            alert('Failed to set the room status to joinable');
            break;
          case errors.roundTimerOver.roundStatus:
            alert('Failed to set the round to results');
            break;
          default:
            alert(`Unknown roundTimerOver error: ${error.error}`);
        }
      }
    });
  }

  onNextRound(room) {
    const round = currentRound(room);

    endRound.call({
      room_id: room._id,
    }, (error, result) => {
      if (error) {
        switch (error.error) {
          case errors.endRound.noRoom:
            alert('The room no longer exists');
            break;
          case errors.endRound.roomStatus:
            alert('Failed to set the room status to joinable');
            break;
          case errors.endRound.roundStatus:
            alert('Failed to end the round');
            break;
          default:
            alert(`Unknown endRound error: ${error.error}`);
        }
      }
    });

    if (isLastRound(round, room)) {
      endGame.call({
        room_id: room._id,
      }, (error, result) => {
        if (error) {
          switch (error.error) {
            case errors.endGame.noRoom:
              alert('The room no longer exists');
              break;
            case errors.endGame.roomStatus:
              alert('Failed to set the room status to complete');
              break;
            default:
              alert(`Unknown endGame error: ${error.error}`);
          }
        }
      });
    } else {
      startRound.call({
        room_id: room._id,
      }, (error, result) => {
        if (error) {
          switch (error.error) {
            case errors.startRound.noRoom:
              alert('The room no longer exists');
              break;
            case errors.startRound.roomStatus:
              alert('Failed to set the room status');
              break;
            case errors.startRound.roundStatus:
              alert('Failed to start the next round');
              break;
            default:
              alert(`Unknown startRound error: ${error.error}`);
          }
        }
      });
    }
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
    } else if (!loading && !room) {
      console.error('Go back to the homepage. Your session is broken.');
      return <ErrorMessage />;
    }

    // Page Rendering
    if (isPreGame(room)) {
      return (
        <HostPreGameScreen 
          room={room}
          onStartGame={this.onStartGame}
        />
      );
    } else if (isPostGame(room)) {
      return (
        <HostEndGameScreen
          room={room}
          getGameScore={getGameScore}
        />
      );
    } else if (isInGame(room)) {
      const round = currentRound(room);
      if (!round) {
        console.error('Theres no current round. What the heck! Something is wrong.');
        return <ErrorMessage />
      }

      if (round.status === 'PRE') {
        return (
          <HostPreRound
            room={room}
            round={currentRound(room)}
            onPlayRound={this.onPlayRound}
          />
        );
      } else if (round.status === 'PLAY') {
        return (
          <HostPlayRound
            round={round}
            room={room}
            onRoundTimerOver={this.onRoundTimerOver}
          />
        );
      } else if (round.status === 'RESULTS') {
        const sketches = _.map(round.sketches, (sketchID) => {
          return Sketches.findOne({ _id: sketchID });
        });
        return (
          <HostRoundResults
            room={room}
            round={currentRound(room)}
            sketches={sketches}
            isLastRound={isLastRound}
            onNextRound={this.onNextRound}
          />
        );
      } else {
        console.error('[Room ' + room._id + ']: Current round in illegal state');
        return <ErrorMessage />;
      }
    } else {
      console.error('[Room ' + room._id + ']: in illegal state');
      return <ErrorMessage />;
    }
  }
}

HostGameScreen.propTypes = {
  loading: React.PropTypes.bool,
  room: React.PropTypes.object,
};
