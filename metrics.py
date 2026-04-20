def all_targets_found(robots, targets):
    found = set()
    for r in robots:
        for t in r.found_targets:
            found.add(t)
    return len(found) == len(targets)


def count_found_targets(robots):
    found = set()
    for r in robots:
        for t in r.found_targets:
            found.add(t)
    return len(found)