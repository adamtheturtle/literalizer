import std.json;
void main() {
auto my_data = JSONValue([
    "true_to_one": JSONValue(["value": JSONValue(1)]),
    "one_to_true": JSONValue(["value": JSONValue(true)]),
    "false_to_zero": JSONValue(["value": JSONValue(0)]),
    "zero_to_false": JSONValue(["value": JSONValue(false)]),
    "nested_boolean_to_float": JSONValue(["value": JSONValue([JSONValue(1.0)])]),
    "nested_float_to_boolean": JSONValue(["value": JSONValue([JSONValue(false)])]),
    "nested_value_types_changed": JSONValue(["value": JSONValue(["nested": JSONValue([JSONValue(true), JSONValue(0)])])]),
    "nested_value_types_reversed": JSONValue(["value": JSONValue(["nested": JSONValue([JSONValue(1), JSONValue(false)])])]),
    "array_order_changed": JSONValue(["value": JSONValue([JSONValue(2), JSONValue(1)])]),
    "array_length_changed": JSONValue(["value": JSONValue([JSONValue(1), JSONValue(2)])]),
    "null_to_zero": JSONValue(["value": JSONValue(0)]),
    "string_to_boolean": JSONValue(["value": JSONValue(true)]),
    "object_key_changed": JSONValue(["value": JSONValue(["b": JSONValue(1)])]),
]);
}
