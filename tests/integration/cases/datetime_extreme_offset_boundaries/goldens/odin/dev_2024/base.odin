#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"2020-06-15T12:00:00-23:59",
	"2020-06-15T12:00:00-18:00",
	"2020-06-15T12:00:00+18:00",
	"2020-06-15T12:00:00+23:59",
}
_ = my_data
}
