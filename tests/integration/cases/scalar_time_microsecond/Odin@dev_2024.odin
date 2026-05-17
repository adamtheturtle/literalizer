#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"exact_millisecond" = "09:30:15.123000",
	"sub_millisecond" = "09:30:15.123456",
}
_ = my_data
}
