#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"value" = map[string]any{"$ref" = "foo"},
}
_ = my_data
}
