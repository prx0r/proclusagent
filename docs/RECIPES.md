# RECIPES — common tasks ($0 unless noted)

## Drain the A-queue (autonomous, $0)
```bash
cd /home/ubuntu/proclusagent
python3 aloop.py --status
python3 aloop.py --until-blocked --max 20 --evolve-loop
```

## Verify the mine ($0)
```bash
python3 aloop.py --evolve
python3 -c "import json,pathlib; ps=list(pathlib.Path('/home/ubuntu/seed0/mine/architectures').rglob('packet.json')); print(len(ps))"
```

## Baseline tournament ($0 local compute)
```bash
cd /home/ubuntu/seed0 && python3 tournament.py seeds/seed1 seeds/seed2 seeds/seed3
```

## Compliance gate ($0)
```bash
cd /home/ubuntu/proclusagent && python3 ../seed0/seed0.py check .
```

## Secret scan before push ($0, must print nothing)
```bash
grep -rIlE "cfat_|ghp_|sk-[A-Za-z0-9]{10,}" --exclude-dir=.git .
```

## R2 list-only survey ($~0, needs env creds, H6/M5 for any pull)
```bash
python3 -c "import boto3,os; s3=boto3.client('s3',endpoint_url=os.environ['R2_ENDPOINT'],aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],region_name='auto'); print([b['Name'] for b in s3.list_buckets()['Buckets']])"
```

## Tournament-test a methodology ($0 collect-only; real agent runs need H4)
```bash
cd /home/ubuntu/seed0
python3 tournament.py seeds/seed1 seeds/seed2 seeds/seed3 seeds/seed4 seeds/seed5 seeds/seed6-ham
python3 funnel.py run --idea "..." --rubric /home/ubuntu/proclusagent/criteria/ham.json --seeds seed6-ham --agent-cmd true --out runs/ham1
python3 funnel.py review --run runs/ham1 --round 1
cd /home/ubuntu/proclusagent && python3 validate_ham.py; echo exit=$?
```
Rule: re-run collect-only after ANY seed move (rubric paths mirror layout).
Full method: `docs/METAGUIDE.md`.

## Predict CLI — usable right now ($0, learns from every press)
```bash
cd /home/ubuntu/proclusagent
printf '\n' | python3 -m predictor.cli --session demo --options ok "verify it" "ship it"
# [1] ok (0.2)  <-- default, Enter accepts / [2] / [3] / pick 1/2/3/Enter/type
# every outcome appends to ./predictor_choices.jsonl (the training data)
# press 3 ten times and "ship it" becomes the Enter default (proven in tests)
```
