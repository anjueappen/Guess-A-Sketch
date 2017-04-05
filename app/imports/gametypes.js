import { prompts as sPrompts } from './sketch-net';

function makeRounds(numRounds, roundTime, prompts) {
  const rounds = [];
  for (let i = 0; i < numRounds; i++) {
    rounds.push({
      time: roundTime,
      index: i,
      // Random choice without replacement
      prompt: prompts.splice(Math.floor(Math.random() * prompts.length), 1)[0],
    });
  }
  return rounds;
}

// Standard gametype.
// N rounds, each the same length of time.
// Picks randomly from all prompts.
const standard = {
  defaults: {
    numRounds: 5,
    roundTime: 25,
    prompts: sPrompts.standard,
  },
};

// Food
const food = {
  defaults: {
    numRounds: standard.defaults.numRounds,
    roundTime: standard.defaults.roundTime,
    prompts: sPrompts.food,
  },
};

// Faster rounds, easy prompts.
const easy = {
  defaults: {
    numRounds: 7,
    roundTime: 15,
    prompts: sPrompts.easy,
  },
};

// Animals, longer drawing time.
const animals = {
  defaults: {
    numRounds: standard.defaults.numRounds,
    roundTime: 40,
    prompts: sPrompts.animals,
  },
};

export const gametypes = {
  standard,
  animals,
  easy,
  food,
};

export const gametype_names = ["standard", "animals", "easy", "food"];

// TO DO: Refactor to use chosen numRounds / roundTime
// Problem: params are undefined
export default function gametype(name, params) {
  const gt = gametypes[name];
  if (!gt) {
    throw Error(`No gametype found named ${name}`);
  }
  const numRounds = params.numRounds || gt.defaults.numRounds;
  const roundTime = params.roundTime || gt.defaults.roundTime;
  const prompts = params.prompts || gt.defaults.prompts;
  console.log(numRounds);
  console.log(params.numRounds);
  const rounds = makeRounds(numRounds, roundTime, prompts);
  return { name, rounds };
}

