/**
 * Created by anjueappen on 3/4/17.
 */
import { Mongo } from 'meteor/mongo';

Rounds = new Mongo.Collection('rounds');
// Rounds.schema = new SimpleSchema({
//   roundID: { type: String, regEx: SimpleSchema.RegEx.Id },
//   prompt: { type: String },
//   sketches: { type: [Sketches.schema], defaultValue: [], minCount: 0 },
// });


