"""Combine declared case context with an axis's rendering options."""

from beartype import beartype
from pydantic import BaseModel

import literalizer


@beartype
def config_with_variant_layout[T: BaseModel](
    *, config: T, layout: literalizer.CollectionLayout
) -> T:
    """Use an axis layout unless the case explicitly chooses its own."""
    if "collection_layout" in config.model_fields_set:
        return config
    return config.model_copy(update={"collection_layout": layout.value})
