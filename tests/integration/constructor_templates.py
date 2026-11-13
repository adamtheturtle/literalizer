"""Resolve native constructor syntax after functional participation."""

from beartype import beartype

from .case_manifests import CaseManifestError, ConstructorCaseSpec


@beartype
def constructor_target_template(
    *, config: ConstructorCaseSpec, language_name: str
) -> str | None:
    """Require a native template for every selected backend."""
    if len(config.target_templates) == 0:
        return config.target_template
    try:
        return config.target_templates[language_name]
    except KeyError as error:
        msg = f"no constructor target template for {language_name!r}"
        raise CaseManifestError(msg) from error
