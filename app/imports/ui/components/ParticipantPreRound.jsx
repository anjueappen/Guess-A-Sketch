import React from 'react';

import BaseComponent from './BaseComponent.jsx';
import ErrorMessage from './ErrorMessage.jsx';
import Prompt from './Prompt.jsx';
import Timer from './Timer.jsx';
import PlayerHeader from './PlayerHeader.jsx';
import {
  Header,
  Container,
  Label,
  Segment,
} from 'semantic-ui-react';

export default class ParticipantPreRound extends BaseComponent {
  constructor(props) {
    super(props);
  }

  render() {
    const {
      room,
      round,
      player,
    } = this.props;

    if (!room || !round) {
      console.error('Received illegal round or room');
      return <ErrorMessage />;
    }

    return (
      <Segment.Group>
        <Segment>
          <PlayerHeader
            text={`Round ${round.index+1}`}
            player={player} />
        </Segment>
        <Segment.Group horizontal>
          <Segment>
            <Prompt prompt={round.prompt} />
          </Segment>
          <Segment> 
            <Timer
              time={3}
              text="Starting in "
              floated="right"
            />
          </Segment>
        </Segment.Group>
      </Segment.Group>
    );
  }
}

ParticipantPreRound.propTypes = {
  room: React.PropTypes.object,
  round: React.PropTypes.object,
  player: React.PropTypes.object,
};
