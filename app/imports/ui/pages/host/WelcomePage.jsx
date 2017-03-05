import React from 'react';
import BaseComponent from '../../components/BaseComponent.jsx';

// will be able to remove import after routing is functional
import {Rooms} from '../../../api/collections/rooms';

export default class WelcomePage extends BaseComponent {
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  onStartGame(event){
    event.preventDefault(); // Don't reload the page
    console.log('Starting Game.');
    // add proper routing functionality here
  }

  render() {
    // for testing - will remove hardcoded room info once routing is functional
    Rooms.insert({ name: 'ABCD' });
    const {
      room = Rooms.findOne({name: 'ABCD'}),
      //room,
    } = this.props;

    let WelcomePage;
    if (room == null) {
      WelcomePage = (
        <h3>Error setting up your room. Please try again.</h3>
      );
    } else {
      WelcomePage = (
        <form onSubmit={this.onStartGame}>
          <h3>Welcome!</h3>
          <p>Room Code: {room.name}</p>
          <button type="submit">Start Game</button>
        </form>
      );
    }

    return WelcomePage; 

  }
}

WelcomePage.propTypes = {
  room: React.PropTypes.object,
};