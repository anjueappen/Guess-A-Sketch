// Host Container
// Responsibilities:
//   Subscribe to relevant collections on the server.
//   Render sub-components based on state.
//   Pass relevant subscription data down through the component hierarchy.

import { Meteor } from 'meteor/meteor';
// XXX: Session
// import { Session } from 'meteor/session';
import { createContainer } from 'meteor/react-meteor-data';

import HostLayout from '../layouts/HostLayout.jsx';

export default createContainer(() => {
  // const publicHandle = Meteor.subscribe('lists.public');
  // const privateHandle = Meteor.subscribe('lists.private');
  console.log('HostContainer creating');
  return {
    user: Meteor.user,
    loading: false,
    connected: Meteor.status().connected,
  };
}, HostLayout);
