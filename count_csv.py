import csv, os
dp = os.path.join(os.path.dirname(__file__), 'uzmorph', 'data')
for f in sorted(os.listdir(dp)):
    if f.endswith('.csv'):
        with open(os.path.join(dp, f), encoding='utf-8') as fh:
            rows = sum(1 for _ in csv.reader(fh)) - 1
        print(f'{f}: {rows} entries')
