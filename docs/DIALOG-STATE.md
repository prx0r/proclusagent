# DIALOG-STATE — assistant-act hypothesis: TESTED, FALSIFIED (2026-09-10)

Method: 99,894 messages time-ordered; 9,044 user sends with a preceding assistant
turn (first text part ≤1200 chars); acts via `predictor/dialog.py`
(confirmation / error / deliverable / other). All local, $0, shapes only.

## Numbers
- P(short-ack|deliverable) = **0.1660** (n=3537)
- P(short-ack|confirmation) = 0.1513 (n=2207) — NOT highest; hypothesis dead
- P(short-ack|error) = 0.1419 (n=1029)
- P(short-ack|other) = 0.1114 (n=2271)
- Base ≈ 0.146. Best lift: +0.02. Auto bar (0.9 precision): not remotely close.

## Reading
Neither side alone predicts your short-acks: not your history (0.195), not the
assistant's last act (0.166 max), not kNN (0.81 accuracy ≈ base). Short-acks are
a JOINT product of (situation × intent) that neither marginal captures — which is
exactly why the product is buttons-with-default (0.67 top-3 family) + post-type
router (0.81), not pre-type auto-send. Gate in `continue_.py` stays CLOSED;
`licensed(0.166, 0.39)` is False and recorded as such.
Next candidate (unbuilt): JOINT features (act × session-phase × project) or the
live choice log both obsolete this debate.
