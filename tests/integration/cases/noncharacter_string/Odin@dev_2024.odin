#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"fffe" = "￾",
	"ffff" = "￿",
}
_ = my_data
}
