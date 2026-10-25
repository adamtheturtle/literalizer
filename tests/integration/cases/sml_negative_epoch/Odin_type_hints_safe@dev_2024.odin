#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"1960-01-01T00:00:00+00:00",
}
_ = my_data
}
