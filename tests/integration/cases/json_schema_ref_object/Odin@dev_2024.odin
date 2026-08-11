#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"schema" = map[string]any{"$ref" = "#/defs/Foo"},
}
_ = my_data
}
