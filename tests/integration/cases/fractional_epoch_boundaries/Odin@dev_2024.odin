#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	"1970-01-01T00:00:00.000001+00:00",
	"1969-12-31T23:59:59.500000+00:00",
	"1970-01-01T00:00:01+00:00",
}
_ = my_data
}
