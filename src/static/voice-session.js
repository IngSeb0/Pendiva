/* Browser speech lifecycle; the visual state follows real playback events. */
(function (root) {
  'use strict';
  function createVoiceSession(options) {
    let generation = 0;
    function stop() {
      generation += 1;
      if (options.synthesis) options.synthesis.cancel();
      options.onChange('idle');
    }
    function speak(text, language) {
      if (!options.synthesis || !options.Utterance) { options.onError(); return false; }
      stop();
      const current = generation;
      const utterance = new options.Utterance(text);
      utterance.lang = language;
      utterance.onstart = () => { if (generation === current) options.onChange('speaking'); };
      utterance.onend = () => { if (generation === current) { options.onChange('idle'); if (options.onEnd) options.onEnd(); } };
      utterance.onerror = () => { if (generation === current) { options.onChange('idle'); options.onError(); } };
      try { options.synthesis.speak(utterance); return true; }
      catch (_) { if (generation === current) { options.onChange('idle'); options.onError(); } return false; }
    }
    return { speak, stop };
  }
  root.PendivaVoice = { createVoiceSession };
  if (typeof module !== 'undefined' && module.exports) module.exports = root.PendivaVoice;
})(typeof window !== 'undefined' ? window : globalThis);
