my_data <- list(
    "true_to_one" = list("value" = 1),
    "one_to_true" = list("value" = TRUE),
    "false_to_zero" = list("value" = 0),
    "zero_to_false" = list("value" = FALSE),
    "nested_boolean_to_float" = list("value" = list(1.0)),
    "nested_float_to_boolean" = list("value" = list(FALSE)),
    "nested_value_types_changed" = list("value" = list("nested" = list(TRUE, 0))),
    "nested_value_types_reversed" = list("value" = list("nested" = list(1, FALSE))),
    "array_order_changed" = list("value" = list(2, 1)),
    "array_length_changed" = list("value" = list(1, 2)),
    "null_to_zero" = list("value" = 0),
    "string_to_boolean" = list("value" = TRUE),
    "object_key_changed" = list("value" = list("b" = 1))
)
