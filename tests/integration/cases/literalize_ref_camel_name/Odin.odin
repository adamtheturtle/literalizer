#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"$ref" = "myVar",
}
_ = my_data
}
