"""Verify retained native outputs and every value mutation without writing files."""
import contextlib
import io
import json
import sys
import tarfile

from scripts.roundtrip_common import verify

MAPPINGS = {"dict", "map", "object", "mapping"}


def keys(value, path=()):
    """Retain key identity independently of mapping-kind tags."""
    if value[0] in MAPPINGS:
        return [(path, key) for key, child in value[1]] + [
            item
            for key, child in value[1]
            for item in keys(child, path + (key,))
        ]
    if value[0] in {"list", "tuple", "array"}:
        return [
            item
            for index, child in enumerate(value[1])
            for item in keys(child, path + (index,))
        ]
    return []


programs = mutations = 0
with tarfile.open(sys.argv[1], "r:gz") as archive:
    def read(name):
        return archive.extractfile(name).read().decode()

    for run in ("final-5493", "final-6569"):
        records = json.loads(read(run + "/results.json"))
        assert len(records) == 1008
        for record in records:
            assert record["classification"] == "pass"
            prefix = run + "/" + record["case"] + "/"
            actual_text = read(prefix + "stdout.txt")
            expected_text = read(prefix + "expected.json")
            actual = json.loads(actual_text)
            verify(label=prefix, produced_json=actual_text,
                   exclude_keys=(), expected_json=expected_text)
            programs += 1
            for kind in ("boolean_type", "negative_zero", "mapping_kind"):
                changed_text = read(prefix + "mutation-" + kind + ".json")
                changed = json.loads(changed_text)
                assert keys(actual["value"]) == keys(changed["value"])
                with contextlib.redirect_stderr(io.StringIO()):
                    try:
                        verify(label=kind, produced_json=changed_text,
                               exclude_keys=(), expected_json=expected_text)
                    except SystemExit as error:
                        assert error.code == 1
                    else:
                        raise AssertionError("oracle accepted " + kind)
                mutations += 1
assert programs == 2016 and mutations == 6048
print(json.dumps({"passing_programs": programs,
                  "rejected_mutations": mutations,
                  "mapping_keys_unchanged": True}))
