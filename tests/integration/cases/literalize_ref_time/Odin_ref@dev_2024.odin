#+feature dynamic-literals
package main

main :: proc() {
my_time := "01:02:03"
my_data := map[string]any{
	"x" = my_time,
}
_ = my_data
}
