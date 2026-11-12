"""Find manifest owners, roles, axes and case names."""

import functools
from collections.abc import Mapping
from pathlib import Path

from beartype import beartype

from .case_manifests import (
    CASE_ROLE_NAMES,
    HETEROGENEOUS_STRATEGY_DEFAULT_ROLE,
    MANIFEST_NAME,
    CaseManifest,
    CaseManifestError,
    CaseRoleName,
    OwnerName,
    load_case_manifests,
)


@functools.cache
@beartype
def case_dir_name_for_owner(*, cases_dir: Path, owner: OwnerName) -> str:
    """Return the name of the sole case directory declaring *owner*.

    Owners naming a single specialized fixture are looked up through
    their manifests, so the fixture's directory name is declared once,
    on disk, rather than restated by the harness.
    """
    names = [
        manifest.case_dir.name
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if manifest.owner == owner
    ]
    match names:
        case [name]:
            return name
        case _:
            msg = (
                f"expected exactly one case with owner {owner!r}, "
                f"found {sorted(names)}"
            )
            raise CaseManifestError(msg)


@functools.cache
@beartype
def case_dir_names_for_variant_axis(
    *,
    cases_dir: Path,
    axis: str,
) -> tuple[str, ...]:
    """Return the names of the case directories declaring *axis*.

    An axis is declared by the inputs it renders, so the set of inputs
    an axis covers is read off the manifests rather than restated.
    """
    return tuple(
        manifest.case_dir.name
        for manifest in load_case_manifests(cases_dir=cases_dir)
        for manifest_variant in manifest.variants
        if manifest_variant.axis == axis
    )


@functools.cache
@beartype
def case_dir_names_for_role(
    *,
    cases_dir: Path,
    role: CaseRoleName,
) -> tuple[str, ...]:
    """Return the names of the case directories declaring *role*.

    Names come back in directory order so a runner's expansion is
    stable.  A role no case answers to is an error rather than an empty
    expansion, so removing the fixture a runner needs fails naming the
    role instead of silently dropping every golden file behind it.
    """
    names = tuple(
        manifest.case_dir.name
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if role in manifest.roles
    )
    if len(names) == 0:
        msg = (
            f"no {MANIFEST_NAME} under {cases_dir} declares roles = [{role!r}]"
        )
        raise CaseManifestError(msg)
    return names


@functools.cache
@beartype
def case_dir_name_for_role(*, cases_dir: Path, role: CaseRoleName) -> str:
    """Return the name of the sole case directory declaring *role*."""
    names = case_dir_names_for_role(cases_dir=cases_dir, role=role)
    match names:
        case (name,):
            return name
        case _:
            msg = (
                f"expected exactly one {MANIFEST_NAME} declaring "
                f"roles = [{role!r}], found {sorted(names)}"
            )
            raise CaseManifestError(msg)


@beartype
def heterogeneous_strategy_role(*, strategy_name: str) -> CaseRoleName:
    """Return the role naming the input *strategy_name* renders.

    Most strategies exercise the mixed-scalar dict holding the default
    role.  A strategy that dict cannot exercise pairs with its own
    input, which declares a role named after the strategy: ``TUPLE``
    needs an input carrying a tuple-eligible heterogeneous scalar array,
    so it renders the fixture declaring
    ``heterogeneous-strategy-tuple-input``.

    A strategy claims its own input by adding that role to the
    vocabulary and to one case, rather than by being named here.
    """
    role = f"heterogeneous-strategy-{strategy_name.lower()}-input"
    for name in CASE_ROLE_NAMES:
        if name == role:
            return name
    return HETEROGENEOUS_STRATEGY_DEFAULT_ROLE


@functools.cache
@beartype
def case_manifests_by_name(cases_dir: Path) -> Mapping[str, CaseManifest]:
    """Return the shared manifest inventory keyed by case directory
    name.
    """
    return {
        manifest.case_dir.name: manifest
        for manifest in load_case_manifests(cases_dir=cases_dir)
    }
