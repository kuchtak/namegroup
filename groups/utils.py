import re
import json

from namegroup.folders.models import Folder
from namegroup.groups.models import NameGroup
from namegroup.groups.models import Name


GROUP_DELIMITERS = ["_"]


def group_names(names_iter):
    unassigned_names = set(names_iter)
    groups = {}

    for name in unassigned_names:
        prefix_parts = re.split("|".join(GROUP_DELIMITERS), name)

        _previous_prefix = ""
        # Create all possible prefixes for the given name
        for idx, prefix_part in enumerate(prefix_parts):
            current_prefix = name[:len(_previous_prefix) + len(prefix_part) + (1 if idx> 0 else 0)]
            _previous_prefix = current_prefix

            if not prefix_part:
                continue

            groups.setdefault(current_prefix, [])
            groups[current_prefix].append(name)

    grouped_names, assigned_names = {}, set()
    # We want to have the biggest group prefix which contain at least two names
    for group_prefix in sorted(groups.keys(), key=len, reverse=True):

        group_names = set(groups[group_prefix]) - assigned_names
        if len(group_names) > 1:
            # Assign tha names to one group
            grouped_names[group_prefix] = list(group_names)

            # Delete name from unassigned names
            for name in group_names:
                assigned_names.add(name)

    # Names which were not assigned they will say alone with their group
    for name in unassigned_names - assigned_names:
        grouped_names[name] = [name]

    return grouped_names


def save_or_update_grouped_names(grouped_names, folder_id=None):
    folder = None
    if folder_id is not None:
        folder = Folder.objects.get(id=folder_id)

    created_objects = []

    for group_prefix, names in grouped_names.items():
        group, created = NameGroup.objects.get_or_create(
            prefix=group_prefix
        )

        for name in names:
            name_obj, reated = Name.objects.get_or_create(
                folder=folder,
                name=name or None,
                defaults=dict(group=group)
            )

            created_objects.append(name_obj)
    return created_objects


if __name__ == "__main__":
    print(json.dumps(group_names(["__a", "a", "adhoc_charge_amt", "adhoc_charge_amt_usd"])))
