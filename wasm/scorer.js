// Genome scorer: mirrors the explicit-vocab linear model (CountVectorizer 1-2grams
// + LogisticRegression). Exact string lookup — no hash ambiguity, wasm-trivial:
// compile this switch/map to wasm32 with the genome baked as constants (tg pattern).
// Usage: node scorer.js <genome.json <fixtures.jsonl> -> JSON predictions.
const fs = require("fs");
function normalize(t) {
  return t.toLowerCase().replace(/\s+/g, " ").trim();
}
function tokens(text) {
  // sklearn token_pattern (?u)\b\w\w+\b : 2+ alnum chars
  return (normalize(text).match(/\b\w\w+\b/gu) || []);
}
function feats(genome, text) {
  const toks = tokens(text);
  const grams = [...toks];
  for (let i = 0; i + 1 < toks.length; i++) grams.push(toks[i] + " " + toks[i + 1]);
  const v = new Map();
  for (const g of grams) {
    const idx = genome.vocab[g];
    if (idx === undefined) continue;
    v.set(idx, (v.get(idx) || 0) + 1);
  }
  return v;
}
function predict(genome, text) {
  const v = feats(genome, text);
  let best = null, bestScore = -Infinity;
  for (let c = 0; c < genome.classes.length; c++) {
    let s = genome.intercept[c];
    const row = genome.coef[c];
    for (const [idx, count] of v) s += (row[idx] || 0) * count;
    if (s > bestScore) { bestScore = s; best = genome.classes[c]; }
  }
  return best;
}
if (require.main === module) {
  const genome = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const lines = fs.readFileSync(process.argv[3] || "/dev/stdin", "utf8").split("\n").filter(Boolean);
  const out = lines.map((l) => predict(genome, JSON.parse(l).ctx));
  process.stdout.write(JSON.stringify(out));
}
module.exports = { tokens, feats, predict };
