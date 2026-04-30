#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a" = map[string]any{"b" = map[string]any{"c" = map[string]any{"$ref" = "deep"}}},
}
_ = my_data
}
