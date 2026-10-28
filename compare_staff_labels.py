#!/usr/bin/env python3
"""Compare the AI-suggested staff labels with a supplied reference file."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

LABELS = {'analysis', 'hot_take', 'reaction'}


def read_csv(path, required):
    with path.open(newline='', encoding='utf-8-sig') as stream:
        reader = csv.DictReader(stream)
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f'{path} must contain columns {sorted(required)}')
        rows = list(reader)
    if len(rows) != 30:
        raise ValueError(f'{path} must contain exactly 30 rows, found {len(rows)}')
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--posts', type=Path, default=Path('data/staff_posts.csv'))
    parser.add_argument('--reference', type=Path, default=Path('data/staff_labels.csv'))
    parser.add_argument('--suggestions', type=Path, default=Path('my_staff_labels.csv'))
    parser.add_argument('--out', type=Path, default=Path('agreement_results.json'))
    args = parser.parse_args()
    if args.out.exists():
        parser.error(f'{args.out} already exists; refusing to overwrite it')
    try:
        posts = read_csv(args.posts, {'id', 'text'})
        reference = read_csv(args.reference, {'id', 'label'})
        suggestions = read_csv(args.suggestions, {'text', 'label'})
        ids = [r['id'] for r in posts]
        reference_ids = [r['id'] for r in reference]
        texts = [r['text'] for r in posts]
        suggestion_texts = [r['text'] for r in suggestions]
        if len(set(ids)) != 30 or len(set(reference_ids)) != 30 or set(ids) != set(reference_ids):
            raise ValueError('Reference IDs must match all 30 unique post IDs exactly')
        if len(set(texts)) != 30 or len(set(suggestion_texts)) != 30 or set(texts) != set(suggestion_texts):
            raise ValueError('Suggestion texts must match all 30 unique posts exactly')
        if any(r['label'] not in LABELS for r in reference + suggestions):
            raise ValueError('Every label must be analysis, hot_take, or reaction')
    except (OSError, ValueError) as error:
        parser.error(str(error))
    reference_by_id = {r['id']: r['label'] for r in reference}
    suggested_by_text = {r['text']: r['label'] for r in suggestions}
    disagreements = [{'id': row['id'], 'text': row['text'],
                      'staff': reference_by_id[row['id']],
                      'mine': suggested_by_text[row['text']]}
                     for row in posts
                     if reference_by_id[row['id']] != suggested_by_text[row['text']]]
    agreed = 30 - len(disagreements)
    result = {'compared': 30, 'agreed': agreed, 'agreement_rate': agreed / 30,
              'disagreements': disagreements, 'staff_posts_not_in_mine': 0,
              'annotation_origin': 'AI-suggested at Juan\'s request; not independent student labels',
              'reference_file_sha256': hashlib.sha256(args.reference.read_bytes()).hexdigest(),
              'reference_label_counts': dict(Counter(r['label'] for r in reference))}
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Compared 30 posts: {agreed} agreements and {len(disagreements)} disagreements.')
    print(f'Result saved to {args.out}. The annotations were AI-suggested, not independent.')
    print('Review every disagreement under the staff taxonomy before writing adjudications.')


if __name__ == '__main__':
    main()
