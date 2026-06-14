/**
 * Ledger line utility — keeps notes within 3 ledger lines of the staff.
 *
 * Each clef's staff covers 9 note positions (5 lines + 4 spaces).
 * A note outside that range needs ledger lines.
 * We enforce a cap of 3 ledger lines above or below.
 */

const NOTE_LETTERS = ['c', 'd', 'e', 'f', 'g', 'a', 'b'];

// Bottom-line note for each clef as [letterIndex, octave]
const CLEF_BOTTOM = {
  treble: [2, 4],  // E4
  bass:   [4, 2],  // G2
  alto:   [3, 3],  // F3
  tenor:  [1, 3],  // D3
};

const MAX_LEDGERS = 3;

/** Convert a VexFlow key like "c/4" or "c#/4" to an absolute position (octave * 7 + letterIdx). */
function keyToPosition(key) {
  const m = key.match(/^([a-g])/i);
  if (!m) return null;
  const letter = m[1].toLowerCase();
  const letterIdx = NOTE_LETTERS.indexOf(letter);
  // Extract octave: digits after "/"
  const octMatch = key.match(/\/(\d+)/);
  const octave = octMatch ? parseInt(octMatch[1], 10) : 4;
  return octave * 7 + letterIdx;
}

/** Staff bottom and top positions for a clef. */
function staffEdges(clef) {
  const [lIdx, oct] = CLEF_BOTTOM[clef] || CLEF_BOTTOM.treble;
  const bottom = oct * 7 + lIdx;
  const top = bottom + 8; // 5 lines = 4 spaces → top line is 8 semitone-letters higher
  return { bottom, top };
}

/** How many ledger lines does a single note need? */
function ledgerLines(clef, key) {
  const pos = keyToPosition(key);
  if (pos === null) return 0;
  const { bottom, top } = staffEdges(clef);
  let ledgers = 0;
  if (pos < bottom) {
    ledgers = Math.ceil((bottom - pos - 1) / 2);
  } else if (pos > top) {
    ledgers = Math.ceil((pos - top - 1) / 2);
  }
  return Math.max(0, ledgers);
}

/** Shift a VexFlow key up or down by an octave (preserves accidental). */
function shiftOctave(key, delta) {
  return key.replace(/\/(\d+)/, (_, oct) => '/' + (parseInt(oct, 10) + delta));
}

/**
 * Given an array of VexFlow keys and a clef, if any note exceeds `maxLedgers`
 * ledger lines, shift ALL notes up or down an octave to bring them within range.
 * Returns the shifted keys (or original if no shift needed).
 */
function clampLedgerLines(clef, keys, maxLedgers = MAX_LEDGERS) {
  if (!keys || keys.length === 0) return keys;
  let tooLow = false;
  let tooHigh = false;
  for (const k of keys) {
    const ll = ledgerLines(clef, k);
    if (ll > maxLedgers) {
      const pos = keyToPosition(k);
      const { bottom, top } = staffEdges(clef);
      if (pos !== null) {
        if (pos < bottom) tooLow = true;
        if (pos > top) tooHigh = true;
      }
    }
  }
  if (!tooLow && !tooHigh) return keys;

  // Pick shift direction: if both too-high and too-low notes exist, shift
  // toward the majority. If tied, shift up by default.
  let delta = 1;
  if (tooLow && !tooHigh) delta = 1;  // notes are too low → shift up
  else if (tooHigh && !tooLow) delta = -1; // notes are too high → shift down

  const shifted = keys.map(k => shiftOctave(k, delta));

  // Re-check after shift; if still out of range, apply a second shift
  for (const k of shifted) {
    if (ledgerLines(clef, k) > maxLedgers) {
      return shifted.map(k2 => shiftOctave(k2, delta));
    }
  }
  return shifted;
}

/**
 * For multi-clef scenarios (e.g., interval with two clefs):
 * Given an array of { key: string, clef: string }, clamp each note
 * independently to its own clef's ledger limit.
 */
function clampMultiClef(notes, maxLedgers = MAX_LEDGERS) {
  // Check if any note is out of range for its clef
  let anyTooLow = false;
  let anyTooHigh = false;
  for (const n of notes) {
    const ll = ledgerLines(n.clef, n.key);
    if (ll > maxLedgers) {
      const pos = keyToPosition(n.key);
      const { bottom, top } = staffEdges(n.clef);
      if (pos !== null) {
        if (pos < bottom) anyTooLow = true;
        if (pos > top) anyTooHigh = true;
      }
    }
  }
  if (!anyTooLow && !anyTooHigh) return notes;

  // Shift all notes together: up if too-low dominates, down if too-high
  let delta = 1;
  if (anyTooLow && !anyTooHigh) delta = 1;
  else if (anyTooHigh && !anyTooLow) delta = -1;

  const shifted = notes.map(n => ({ ...n, key: shiftOctave(n.key, delta) }));

  // Second pass if needed
  for (const n of shifted) {
    if (ledgerLines(n.clef, n.key) > maxLedgers) {
      return shifted.map(n2 => ({ ...n2, key: shiftOctave(n2.key, delta) }));
    }
  }
  return shifted;
}

module.exports = {
  NOTE_LETTERS,
  CLEF_BOTTOM,
  MAX_LEDGERS,
  keyToPosition,
  staffEdges,
  ledgerLines,
  shiftOctave,
  clampLedgerLines,
  clampMultiClef,
};
