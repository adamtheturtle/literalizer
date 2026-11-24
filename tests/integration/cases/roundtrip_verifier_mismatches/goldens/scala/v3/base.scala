object Fixture_roundtrip_verifier_mismatches_Scala {
val my_data = Map(
    "true_to_one" -> Map("value" -> 1),
    "one_to_true" -> Map("value" -> true),
    "false_to_zero" -> Map("value" -> 0),
    "zero_to_false" -> Map("value" -> false),
    "nested_boolean_to_float" -> Map("value" -> List[Double](1.0)),
    "nested_float_to_boolean" -> Map("value" -> List[Boolean](false)),
    "nested_value_types_changed" -> Map("value" -> Map("nested" -> List(true, 0))),
    "nested_value_types_reversed" -> Map("value" -> Map("nested" -> List(1, false))),
    "array_order_changed" -> Map("value" -> List[Int](2, 1)),
    "array_length_changed" -> Map("value" -> List[Int](1, 2)),
    "null_to_zero" -> Map("value" -> 0),
    "string_to_boolean" -> Map("value" -> true),
    "object_key_changed" -> Map("value" -> Map("b" -> 1)),
)
}
