"""Compare two .pbit packages entry by entry and show how the differing entries differ.
Usage: python -I diff_pbit.py <a.pbit> <b.pbit>"""
import difflib
import json
import sys
import zipfile


def json_diff(x, y, path="$"):
    """Yield (path, a, b) for every leaf where two JSON values differ."""
    if type(x) is not type(y):
        yield path, x, y
    elif isinstance(x, dict):
        for k in sorted(set(x) | set(y)):
            if k not in x or k not in y:
                yield f"{path}.{k}", x.get(k, "<absent>"), y.get(k, "<absent>")
            else:
                yield from json_diff(x[k], y[k], f"{path}.{k}")
    elif isinstance(x, list):
        if len(x) != len(y):
            yield f"{path}[len]", len(x), len(y)
        for i, (p, q) in enumerate(zip(x, y)):
            yield from json_diff(p, q, f"{path}[{i}]")
    elif x != y:
        yield path, x, y


def text(raw):
    if raw[:2] == b"\xff\xfe" or (len(raw) > 1 and raw[1:2] == b"\x00"):
        return raw.decode("utf-16-le", "ignore")
    return raw.decode("utf-8", "ignore")


a, b = (zipfile.ZipFile(p) for p in sys.argv[1:3])
na, nb = set(a.namelist()), set(b.namelist())
print("only in a:", sorted(na - nb))
print("only in b:", sorted(nb - na))
same = 0
for n in sorted(na & nb):
    ra, rb = a.read(n), b.read(n)
    if ra == rb:
        same += 1
        continue
    print(f"DIFFERS: {n}")
    try:
        ja, jb = json.loads(text(ra)), json.loads(text(rb))
        for path, va, vb in json_diff(ja, jb):
            print(f"    {path}\n      a: {str(va)[:300]}\n      b: {str(vb)[:300]}")
        continue
    except ValueError:
        pass
    ta, tb = text(ra).splitlines(), text(rb).splitlines()
    for line in difflib.unified_diff(ta, tb, lineterm="", n=0):
        if line.startswith(("---", "+++", "@@")):
            continue
        print("   ", line[:220])
print("identical entries:", same)
