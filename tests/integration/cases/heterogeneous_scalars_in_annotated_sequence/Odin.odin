#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	true,
	1.5,
	nil,
	"2020-01-01",
	"2020-01-01T00:00:00+00:00",
	[dynamic]any{},
}
_ = my_data
}
