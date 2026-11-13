#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"true_to_one" = map[string]any{"value" = 1},
	"one_to_true" = map[string]any{"value" = true},
	"false_to_zero" = map[string]any{"value" = 0},
	"zero_to_false" = map[string]any{"value" = false},
	"nested_boolean_to_float" = map[string]any{"value" = [dynamic]any{1.0}},
	"nested_float_to_boolean" = map[string]any{"value" = [dynamic]any{false}},
	"nested_value_types_changed" = map[string]any{"value" = map[string]any{"nested" = [dynamic]any{true, 0}}},
	"nested_value_types_reversed" = map[string]any{"value" = map[string]any{"nested" = [dynamic]any{1, false}}},
	"array_order_changed" = map[string]any{"value" = [dynamic]any{2, 1}},
	"array_length_changed" = map[string]any{"value" = [dynamic]any{1, 2}},
	"null_to_zero" = map[string]any{"value" = 0},
	"string_to_boolean" = map[string]any{"value" = true},
	"object_key_changed" = map[string]any{"value" = map[string]any{"b" = 1}},
}
_ = my_data
}
