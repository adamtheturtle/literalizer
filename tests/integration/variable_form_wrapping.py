"""Helpers that produce a default ``NewVariable`` form per language."""

import literalizer


def wrap_variable_name(lang_cls: literalizer.LanguageCls) -> str | None:
    """Return the wrap variable name for a language class."""
    return "my_data" if lang_cls.supports_variable_names else None


def wrap_variable_form(
    lang_cls: literalizer.LanguageCls,
) -> literalizer.NewVariable | None:
    """Return a :class:`NewVariable` form for a language class, or
    None.
    """
    name = wrap_variable_name(lang_cls=lang_cls)
    if name is None:
        return None
    return literalizer.NewVariable(name=name)
