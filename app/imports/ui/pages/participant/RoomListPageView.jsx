import React from 'react';

import BaseComponent from '../../components/BaseComponent.jsx';
import NoRooms from '../../components/NoRooms.jsx';
import RoomItem from '../../components/RoomItem.jsx';
import PlayerHeader from '../../components/PlayerHeader.jsx';
import {
  Container,
  Header,
  Icon,
  Card,
  Segment,
} from 'semantic-ui-react';


export default class RoomListPageView extends BaseComponent {
  constructor(props) {
    super(props);
  }

  render() {
    const {
      loading,
      rooms,
      player,
      onRoomClickHandler,
    } = this.props;

    if (loading) {
      return <p>Loading...</p>;
    } else if (!rooms || rooms.length === 0) {
      return <NoRooms />;
    } else {
      rooms.sort((a, b) => {
        if (!a.players) {
          return -1;
        } else if (!b.players) {
          return 1;
        } else {
          return a.players.length - b.players.length;
        }
      });
      const joinable = rooms
        .filter(room => room.status === 'JOINABLE')
        .map(room => (
          <RoomItem
            key={room._id}
            onClick={onRoomClickHandler}
            room={room}
          />
        ));
      const playing = rooms
        .filter(room => room.status === 'PLAYING')
        .map(room => (
          <RoomItem
            key={room._id}
            room={room}
          />
        ));
      return (
        <Segment.Group>
          <Segment>
            <PlayerHeader text="Rooms" player={player} />
          </Segment>
          <Segment>
            <Card.Group
              itemsPerRow={2} >
              {joinable}
            </Card.Group>
          </Segment>
          <Segment disabled>
            <Card.Group
              itemsPerRow={2} >
              {playing}
            </Card.Group>
          </Segment>
        </Segment.Group>
      );
    }
  }
}

RoomListPageView.propTypes = {
  loading: React.PropTypes.bool,
  rooms: React.PropTypes.array,
  player: React.PropTypes.object,
  onRoomClickHandler: React.PropTypes.func,
};
