#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"$ref" = "schema.json",
}
_ = my_data
}
