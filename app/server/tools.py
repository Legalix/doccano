import csv

from server.models import Label


LABEL_COLUMN_MAP = {
    'project_id': lambda x: int(x['Project']),
    'text': lambda x: x['Etiqueta'],
    'prefix_key': lambda x: x['Prefix key'],
    'suffix_key': lambda x: x['Suffix key'],
    'background_color': lambda x: x['Color'],
}


def create_label(**attributes):
    """
    """
    if Label.objects.filter(**attributes).exists():
        return None
    return Label.objects.create(**attributes)


def print_labels(labels):
    """
    """
    labels_text = '\n'.join(
        f'id: {l.id}, text: {l.text}, color: {l.background_color}, shortcut: {l.prefix_key} + {l.suffix_key}'
        for l in filter(None, labels)
    )
    print(f'The following labels were created:\n\n{labels_text}')


def upload_labels(destination_project_id: int, csv_filename: str):
    """
    """
    with open(csv_filename) as csv_file:
        reader = csv.DictReader(csv_file)
        created_labels = [
            create_label(
                **{
                    column_name: getter(row)
                    for column_name, getter in LABEL_COLUMN_MAP.items()
                }
            ) for row in reader
        ]

    print_labels(created_labels)


def copy_labels(source_project_id: int, destination_project_id: int):
    """
    """
    created_labels = []
    for label in Label.objects.filter(project_id=source_project_id).iterator():
        item = {
            field: getattr(label, field)
            for field in LABEL_COLUMN_MAP
        }
        item['project_id'] = destination_project_id
        created_labels.append(create_label(**item))

    print_labels(created_labels)
