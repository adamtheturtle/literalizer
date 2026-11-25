#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"foo",
	"bar",
	"baz",
}
_ = my_data
}
