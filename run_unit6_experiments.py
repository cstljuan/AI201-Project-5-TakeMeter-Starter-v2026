"""Run the course notebook's training functions without overwriting Unit 5 outputs."""
import argparse
import ast
import gc
import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')
os.environ.setdefault('HF_HUB_DISABLE_TELEMETRY', '1')

import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, set_seed

LABELS = ['supported_claim', 'unsupported_claim', 'help_request', 'guide_or_solution']
BASE_MODEL = 'distilbert-base-uncased'
MAX_LENGTH = 128
BATCH_SIZE = 8
SEEDS = [42, 7, 2024]
DEVICE = 'cuda' if torch.cuda.is_available() else ('mps' if torch.backends.mps.is_available() else 'cpu')
DEVICE_NAME = torch.cuda.get_device_name(0) if DEVICE == 'cuda' else ('Apple Silicon GPU (MPS)' if DEVICE == 'mps' else 'CPU')

# Extract only the reviewed function definitions. Notebook cells also execute the
# Unit 5 training and overwrite results.json and test_split.csv if run whole.
notebook = json.loads(Path('takemeter.ipynb').read_text())
for cell_index in (12, 14, 16):
    source = ''.join(notebook['cells'][cell_index]['source'])
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    module = ast.fix_missing_locations(ast.Module(body=functions, type_ignores=[]))
    exec(compile(module, f'takemeter.ipynb:cell-{cell_index}', 'exec'), globals())

parser = argparse.ArgumentParser()
parser.add_argument('--run-label', choices=['before', 'after', 'after_second'], required=True)
parser.add_argument('--epochs', type=int, default=3)
parser.add_argument('--learning-rate', type=float, default=2e-5)
parser.add_argument('--max-length', type=int, default=128)
args = parser.parse_args()
assert args.epochs > 0 and args.learning_rate > 0 and 1 <= args.max_length <= 512
MAX_LENGTH = args.max_length
output = Path(f'results_three_seeds_{args.run_label}.json')
examples_file = Path(f'predictions_three_seeds_{args.run_label}.json')
if output.exists() or examples_file.exists():
    raise SystemExit('Output exists. Refusing to overwrite an existing experiment.')

frame = pd.read_csv('labels.csv')
assert set(frame.label) == set(LABELS) and not frame.text.duplicated().any()
results, examples = [], []
checkpoint_dir = Path(os.environ.get('TAKEMETER_CHECKPOINT_DIR', '.'))
checkpoint_dir.mkdir(parents=True, exist_ok=True)
for seed in SEEDS:
    print(f'\nRunning {args.run_label}: seed {seed} on {DEVICE_NAME}', flush=True)
    train, validation, test = split_dataset(frame, seed)
    trainer, tokenizer = train_model(train, validation, LABELS, seed, args.epochs,
                                     args.learning_rate, BATCH_SIZE, BASE_MODEL, quiet=True)
    result = evaluate(trainer, tokenizer, test, LABELS, seed=seed)
    result.update(device=DEVICE, device_name=DEVICE_NAME, torch_version=torch.__version__,
                  max_length=MAX_LENGTH, epochs=args.epochs, learning_rate=args.learning_rate,
                  batch_size=BATCH_SIZE, dataset_sha256=hashlib.sha256(Path('labels.csv').read_bytes()).hexdigest())
    def tokenize(batch):
        return tokenizer(batch['text'], truncation=True, padding='max_length', max_length=MAX_LENGTH)
    ds = Dataset.from_pandas(to_ids(test, LABELS)).map(tokenize, batched=True)
    logits = trainer.predict(ds).predictions
    probabilities = np.exp(logits - logits.max(axis=-1, keepdims=True))
    probabilities /= probabilities.sum(axis=-1, keepdims=True)
    guessed = probabilities.argmax(axis=-1)
    for i, row in test.iterrows():
        examples.append({'seed': seed, 'text': row['text'], 'true_label': row['label'],
                         'predicted_label': LABELS[int(guessed[i])],
                         'confidence': float(probabilities[i, guessed[i]])})
    results.append(result)
    (checkpoint_dir / f'{args.run_label}-partial-results.json').write_text(json.dumps(results, indent=2) + '\n')
    (checkpoint_dir / f'{args.run_label}-partial-predictions.json').write_text(json.dumps(examples, indent=2) + '\n')
    print(f"Seed {seed}: accuracy {result['accuracy']:.3f}, macro F1 {result['f1_macro']:.3f}", flush=True)
    del trainer, tokenizer, ds
    gc.collect()
    if DEVICE == 'mps':
        torch.mps.empty_cache()

output.write_text(json.dumps(results, indent=2) + '\n')
examples_file.write_text(json.dumps(examples, indent=2) + '\n')
print(f'Saved {output} and {examples_file}', flush=True)
