const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const template = fs.readFileSync(path.join(__dirname, '../preview/kk-Arab/template.html'), 'utf8');
const start = template.indexOf('const LATN_QWERTY4=');
const end = template.indexOf('const SCRIPT_INFO=', start);
assert(start >= 0 && end > start, 'Latin layout definitions must exist');
const context = {};
vm.runInNewContext(template.slice(start, end) + ';globalThis.layouts=LATN_LAYOUTS;globalThis.select=latinLayout;', context);
const layouts = JSON.parse(JSON.stringify(context.layouts));
const letters = row => row.filter(t => !t.startsWith('\\s{'));
const upper = c => c === 'i' ? 'İ' : c === 'ı' ? 'I' : c.toUpperCase();
const alphabet = [...'abcdefghijklmnopqrstuvwxyzäğıñöşūü'].sort();
const qwerty = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm'];
const cases = [
  {count: 29, rows: [11, 10, 8], hidden: {a:'ä', o:'ö', s:'ş', u:'ū', y:'ü'}, units:[11,10,10]},
  {count: 30, rows: [11, 11, 8], hidden: {a:'ä', o:'ö', u:'ū', y:'ü'}, units:[11,11,11]},
  {count: 31, rows: [11, 11, 9], hidden: {a:'ä', o:'ö', u:'ū'}, units:[11,11,11]},
];

for (const expected of cases) {
  const id = `qwerty${expected.count}`;
  test(`${expected.count} letters: exact rows, QWERTY order and full alphabet access`, () => {
    const layout = layouts[id];
    const rows = layout.default.map(letters);
    assert.deepEqual(rows.map(r=>r.length), expected.rows);
    assert.equal(rows.flat().length, expected.count);
    assert.equal(new Set(rows.flat()).size, expected.count);
    rows.forEach((row,i) => assert.equal(row.filter(c=>/^[a-z]$/.test(c)).join(''), qwerty[i]));
    assert.deepEqual([...new Set([...rows.flat(), ...Object.values(expected.hidden)])].sort(), alphabet);
    assert.equal(layout.default[2][0], '\\s{shift}');
    assert.equal(layout.default[2].at(-1), '\\s{backspace}');
  });

  test(`${expected.count} letters: exact lowercase and uppercase long-press mappings`, () => {
    const layout = layouts[id];
    const mappings = {};
    for (const [base, alt] of Object.entries(expected.hidden)) {
      mappings[base] = [alt];
      mappings[upper(base)] = [upper(alt)];
    }
    assert.deepEqual(layout.longpress, mappings);
    for (const [layer, isUpper] of [['default',false],['shift',true]]) {
      const visible = new Set(layout[layer].flatMap(letters));
      for (const [base, alternatives] of Object.entries(layout.longpress)) {
        if (visible.has(base)) for (const alt of alternatives) assert(!visible.has(alt), `${alt} should require long-press`);
      }
      const reached = [...visible, ...Object.entries(layout.longpress).filter(([base])=>visible.has(base)).flatMap(([,alts])=>alts)];
      const expectedAlphabet = isUpper ? alphabet.map(upper).sort() : alphabet;
      assert.deepEqual([...new Set(reached)].sort(), expectedAlphabet);
    }
    assert.deepEqual(layout.longpress.w, undefined, 'ü stays on y; w has no alternative');
  });

  test(`${expected.count} letters: Turkic I casing and equal letter units`, () => {
    const layout = layouts[id];
    assert.deepEqual(layout.shift, layout.default.map(row=>row.map(t=>t.startsWith('\\s{')?t:upper(t))));
    assert.equal(layout.geometry.baseCount, 11);
    const units = layout.default.map((row,i)=>row.length+(i===2?2*(layout.geometry.edgeWeight-1):0));
    assert.deepEqual(units, expected.units);
    assert.equal(layout.geometry.edgeWeight, expected.count===30?1.5:1);
  });
}

test('kazakh-compact replaces only w/x/c and preserves a 26-letter budget', () => {
  const layout = layouts['kazakh-compact'];
  assert.deepEqual(layout.default.map(row=>letters(row).join('')), ['qüertyuiop', 'asdfghjkl', 'zşğvbnm']);
  assert.equal(new Set(layout.default.flatMap(letters)).size, 26);
  assert.equal(layout.default[2][0], '\\s{shift}');
  assert.equal(layout.default[2].at(-1), '\\s{backspace}');
  assert.deepEqual(layout.shift, layout.default.map(row=>row.map(t=>t.startsWith('\\s{')?t:upper(t))));
  assert.equal(layout.geometry.baseCount, 10);
  assert.equal(layout.geometry.edgeWeight, 1.5);
});

test('kazakh-compact keeps every letter reachable once in both cases, including displaced ASCII', () => {
  const layout = layouts['kazakh-compact'];
  for (const [layer, capital] of [['default',false],['shift',true]]) {
    const visible = layout[layer].flatMap(letters);
    const hidden = visible.flatMap(base=>layout.longpress[base]||[]);
    const expected = capital ? alphabet.map(upper).sort() : alphabet;
    assert.deepEqual([...visible, ...hidden].sort(), expected);
    for (const [base, alt] of Object.entries({ü:'w', ş:'x', ğ:'c'})) {
      assert.deepEqual(layout.longpress[capital?upper(base):base], [capital?upper(alt):alt]);
    }
  }
  for (const base of ['g','s','y','G','S','Y']) assert.equal(layout.longpress[base], undefined);
});

test('The selector resolves all variants and falls back to QWERTY4', () => {
  for (const id of Object.keys(layouts)) {
    context.latinVariant = id;
    assert.strictEqual(context.select(), context.layouts[id]);
    assert(template.includes(`data-latin-variant="${id}"`), `${id} needs a visible selector`);
  }
  context.latinVariant = 'unknown';
  assert.strictEqual(context.select(), context.layouts.qwerty4);
  assert.equal(layouts.qwerty3.default.flatMap(letters).length, 26);
  assert.equal(layouts.qwerty4.extraDefault.length, 8);
});
