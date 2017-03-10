import React from 'react';
import BaseComponent from '../../components/BaseComponent.jsx';
import { Session } from 'meteor/session';
import { browserHistory } from 'react-router';

import { changeRoomStatus, changeRoundStatus } from '/imports/api/methods';
import PlayerItem from '../../components/PlayerItem.jsx';
import { HOST_ROOM } from '/imports/api/session';

export default class WelcomePage extends BaseComponent {
    constructor(props) {
        super(props);
        this.props = props;
    }

    onStartGame(event){
        event.preventDefault(); // Don't reload the page
        console.log('Starting Game.');

        let room = Session.get(HOST_ROOM);

        // change room status if we're playing for the first time
        if (room.nextRoundIndex == 0){
          const didChangeRoomStatus = changeRoomStatus.call({
            room_id: room._id,
            room_status: "PLAYING"
          });
          if (!didChangeRoomStatus) {
            console.error('Unable to change room status. Server rejected request.');
            return;
          }
        }

        // change round status
        const didChangeRoundStatus = changeRoundStatus.call({
          room_id: room._id,
          round_index: room.nextRoundIndex,
          round_status: "PLAYING"
        });
        if (!didChangeRoundStatus) {
          console.error('Unable to change round status. Server rejected request.');
          return;
        }

        browserHistory.push('/host/play');
    }

    render() {
        const {
          loading,
          room
        } = this.props;

        if (!room) {
          return (
            <div>
              <p>Error setting up your room. Please try again.</p>
            </div>
          );
        } else if (loading) {
          // Early return
          return (
            <h3>Loading...</h3>
          );
        }

        let player_list = 'N/A';
        if (room.players.length > 0) {
          player_list = room.players.map(function(player,index) {
            return (
              <PlayerItem 
              key = {player._id} // warning about key here
              text = {player.name} />
            );
          });
        }

        return (
            <form onSubmit={this.onStartGame}>
              <h3>Welcome!</h3>
              <p>Room Name: {room.name}</p>
              <p>Room Code: {room._id.substring(0, 4)}</p>
              <p>Players in Room: </p>
              <div> {player_list} </div>
              <button type="submit">Start Game</button>
            </form>
        );
    }
}

WelcomePage.propTypes = {
  room: React.PropTypes.object,
  loading: React.PropTypes.bool,
};
