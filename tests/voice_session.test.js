'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { createVoiceSession } = require('../src/static/voice-session.js');

test('voice state follows playback, and stopping ignores late events', () => {
  const states = [], utterances = [];
  class Utterance { constructor(text) { this.text = text; } }
  const synthesis = { cancel() {}, speak(utterance) { utterances.push(utterance); } };
  const voice = createVoiceSession({synthesis, Utterance, onChange: state => states.push(state), onError: () => assert.fail('unexpected speech error')});
  assert.equal(voice.speak('Hola', 'es-CO'), true);
  assert.equal(utterances[0].lang, 'es-CO');
  utterances[0].onstart();
  assert.equal(states.at(-1), 'speaking');
  voice.stop();
  assert.equal(states.at(-1), 'idle');
  utterances[0].onstart();
  utterances[0].onend();
  assert.equal(states.at(-1), 'idle');
  voice.speak('Hello', 'en-US');
  utterances[1].onstart();
  utterances[1].onend();
  assert.equal(states.at(-1), 'idle');
});

test('natural playback completion resumes the voice loop but manual stop does not', () => {
  const utterances = []; let completed = 0;
  class Utterance {}
  const voice = createVoiceSession({synthesis:{cancel(){},speak(item){utterances.push(item)}},Utterance,
    onChange:()=>{},onEnd:()=>completed++,onError:()=>assert.fail('unexpected speech error')});
  voice.speak('Pregunta', 'es-CO');
  utterances[0].onend();
  assert.equal(completed,1);
  voice.speak('Detener', 'es-CO');
  voice.stop();
  utterances[1].onend();
  assert.equal(completed,1);
});

test('missing or failed speech reports an error without claiming it is speaking', () => {
  const states = []; let errors = 0;
  const voice = createVoiceSession({synthesis: null, Utterance: null, onChange: state => states.push(state), onError: () => errors++});
  assert.equal(voice.speak('Hola', 'es-CO'), false);
  assert.equal(errors, 1);
  assert.equal(states.includes('speaking'), false);
  class Utterance {}
  const failing = createVoiceSession({synthesis: {cancel() {}, speak() {throw Error('blocked');}}, Utterance, onChange: state => states.push(state), onError: () => errors++});
  assert.equal(failing.speak('Hola', 'es-CO'), false);
  assert.equal(errors, 2);
  assert.equal(states.at(-1), 'idle');
});
