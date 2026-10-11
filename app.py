
import sys
import re
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import Store, form, heading, note, table, run


store = Store(
    Path(__file__).with_name('data.json'),
    {'reports': []}
)


# Common words that do not help much in identifying an item
STOP_WORDS = {
    'a', 'an', 'the', 'is', 'are', 'was', 'were',
    'i', 'my', 'me', 'it', 'this', 'that', 'and',
    'or', 'of', 'in', 'on', 'at', 'to', 'for',
    'with', 'near', 'found', 'lost', 'have', 'has',
    'from', 'by', 'as', 'be', 'been', 'being'
}


def extract_words(description, ignore_common=True):
    """Extract words from a description."""
    words = set(re.findall(r'\w+', description.lower()))

    if ignore_common:
        words = words - STOP_WORDS

    return words


def matches(report, reports, ignore_common=True):
    """
    Find possible matches for a Lost or Found report.

    Original algorithm: ignore_common=False
    Improved algorithm: ignore_common=True
    """
    results = []

    words = extract_words(
        report['description'],
        ignore_common
    )

    for other in reports:

        # Do not match reports of the same kind
        if other['kind'] == report['kind']:
            continue

        # Skip reports that have already been returned
        if other['status'] == 'Returned':
            continue

        # Category must be the same
        if other['category'].lower() != report['category'].lower():
            continue

        other_words = extract_words(
            other['description'],
            ignore_common
        )

        shared = words & other_words

        # Base score for the same category
        score = 3
        reasons = ['Same category']

        # Score for shared description words
        if shared:
            score += len(shared)

            if ignore_common:
                reasons.append(
                    'Shared meaningful words: '
                    + ', '.join(sorted(shared))
                )
            else:
                reasons.append(
                    'Shared words: '
                    + ', '.join(sorted(shared))
                )

        # Score for the same location
        if other['location'].lower() == report['location'].lower():
            score += 2
            reasons.append('Same location')

        # Score when dates are within three days
        gap = abs(
            (
                date.fromisoformat(report['date'])
                - date.fromisoformat(other['date'])
            ).days
        )

        if gap <= 3:
            score += 1
            reasons.append('Dates within 3 days')

        results.append([
            other['id'],
            score,
            '; '.join(reasons),
            other['description']
        ])

    return sorted(
        results,
        key=lambda row: (-row[1], row[0])
    )


def sample_reports():
    """Create ten sample reports for algorithm comparison."""

    samples = [
        (1, 'Lost', 'Bottle',
         'I lost a blue bottle in the library',
         'Library', '2026-10-01'),

        (2, 'Found', 'Bottle',
         'The blue bottle was found in a library',
         'Library', '2026-10-02'),

        (3, 'Lost', 'Bag',
         'I lost a black college bag near the classroom',
         'Classroom', '2026-10-03'),

        (4, 'Found', 'Bag',
         'The black college bag is near the classroom',
         'Classroom', '2026-10-04'),

        (5, 'Lost', 'Book',
         'I lost the Python programming book',
         'Hostel', '2026-10-05'),

        (6, 'Found', 'Book',
         'A Python programming book was found',
         'Hostel', '2026-10-06'),

        (7, 'Lost', 'Keys',
         'I lost my three metal keys',
         'Canteen', '2026-10-07'),

        (8, 'Found', 'Keys',
         'The three metal keys are at the canteen',
         'Canteen', '2026-10-08'),

        (9, 'Lost', 'Bottle',
         'My red water bottle has a silver cap',
         'Sports Ground', '2026-10-09'),

        (10, 'Found', 'Bottle',
         'A red water bottle with a silver cap',
         'Sports Ground', '2026-10-10')
    ]

    reports = []

    for item in samples:
        reports.append({
            'id': item[0],
            'kind': item[1],
            'category': item[2],
            'description': item[3],
            'location': item[4],
            'date': item[5],
            'status': 'Reported'
        })

    return reports


def compare_algorithms():
    """
    Compare the original and improved algorithms
    using ten sample reports.
    """

    reports = sample_reports()
    comparison_rows = []

    for report in reports:

        # Compare Lost reports against Found reports
        if report['kind'] != 'Lost':
            continue

        original_results = matches(
            report, reports, ignore_common=False
        )

        improved_results = matches(
            report, reports, ignore_common=True
        )

        original_scores = {
            row[0]: row[1] for row in original_results
        }

        improved_scores = {
            row[0]: row[1] for row in improved_results
        }

        for found_id in original_scores:

            old_score = original_scores[found_id]
            new_score = improved_scores[found_id]

            found_report = next(
                r for r in reports if r['id'] == found_id
            )

            if new_score < old_score:
                change = 'Common words removed'
            elif new_score == old_score:
                change = 'No score change'
            else:
                change = 'Score increased'

            comparison_rows.append([
                report['id'],
                found_id,
                old_score,
                new_score,
                change
            ])

    return (
        heading('Ten Sample Reports: Algorithm Comparison')
        + note(
            'Original = counts all shared words. '
            'Improved = ignores common words. '
            'Both algorithms retain the same category, '
            'location and date scoring rules.'
        )
        + table(
            [
                'Lost ID',
                'Found ID',
                'Original Score',
                'Improved Score',
                'Comparison'
            ],
            comparison_rows
        )
    )


def view():
    today = date.today().isoformat()

    out = note(
        'Use sample descriptions without contact details. '
        'Matching suggests candidates; it does not prove ownership.'
    )

    out += form(
        'add',
        [
            ('kind', 'Report type', 'select', ['Lost', 'Found']),
            ('category', 'Category', 'text', 'Bottle'),
            ('description', 'Description', 'text', 'Blue steel bottle'),
            ('location', 'Location', 'text', 'Library'),
            ('date', 'Date', 'date', today)
        ],
        'Add report'
    )

    out += form(
        'search',
        [('query', 'Category or description keyword', 'text', 'bottle')],
        'Search reports'
    )

    out += form(
        'match',
        [('id', 'Lost or found report ID', 'number', '1')],
        'Suggest matches'
    )

    out += form(
        'status',
        [
            ('id', 'Report ID', 'number', '1'),
            (
                'status',
                'New status',
                'select',
                ['Reported', 'Matched', 'Returned']
            )
        ],
        'Update status'
    )

    # Student extension: compare both matching algorithms
    out += form(
        'compare',
        [],
        'Compare algorithms on 10 sample reports'
    )

    out += heading('All reports') + table(
        [
            'ID', 'Kind', 'Category', 'Description',
            'Location', 'Date', 'Status'
        ],
        [list(r.values()) for r in store.data['reports']]
    )

    return out


def handle(data):
    records = store.data['reports']
    action = data['action']

    if action == 'compare':
        return compare_algorithms()

    if action == 'add':
        date.fromisoformat(data['date'])

        if data['kind'] not in ['Lost', 'Found']:
            raise ValueError('Choose Lost or Found.')

        for key in ['category', 'description', 'location']:
            if not data[key].strip():
                raise ValueError('Text fields cannot be blank.')

        record = {
            'id': max(
                (r['id'] for r in records),
                default=0
            ) + 1,
            'kind': data['kind'],
            'category': data['category'].strip(),
            'description': data['description'].strip(),
            'location': data['location'].strip(),
            'date': data['date'],
            'status': 'Reported'
        }

        records.append(record)

    elif action == 'search':
        query = data['query'].strip().lower()

        found = [
            list(r.values())
            for r in records
            if query in (
                r['category'] + ' ' + r['description']
            ).lower()
        ]

        return heading('Filtered reports') + table(
            [
                'ID', 'Kind', 'Category', 'Description',
                'Location', 'Date', 'Status'
            ],
            found
        )

    elif action in ['match', 'status']:
        try:
            report_id = int(data['id'])
        except (ValueError, TypeError):
            raise ValueError('Enter a valid report ID.')

        record = next(
            (r for r in records if r['id'] == report_id),
            None
        )

        if record is None:
            raise ValueError('Report ID does not exist.')

        if action == 'match':
            if record['status'] == 'Returned':
                raise ValueError('This report is already closed.')

            results = matches(
                record,
                records,
                ignore_common=True
            )

            return heading('Possible matches') + table(
                ['ID', 'Score', 'Reasons', 'Description'],
                results
            )

        if data['status'] not in [
            'Reported', 'Matched', 'Returned'
        ]:
            raise ValueError('Invalid status.')

        record['status'] = data['status']

    else:
        raise ValueError('Unknown action.')

    store.save()


if __name__ == '__main__':
    run('Campus Lost and Found Matcher', view, handle)