"""Resolve native constructor syntax after functional participation."""

from beartype import beartype

from .case_manifests import CaseManifestError, ConstructorCaseSpec


@beartype
def constructor_target_template(
    *, config: ConstructorCaseSpec, language_name: str
) -> str | None:
    """Resolve native syntax, falling back to explicitly shared input."""
    if len(config.target_templates) == 0:
        return None
    try:
        return config.target_templates[language_name]
    except KeyError as error:
        if config.target_source_template is not None or config.target_variable:
            return None
        msg = f"no constructor target template for {language_name!r}"
        raise CaseManifestError(msg) from error
