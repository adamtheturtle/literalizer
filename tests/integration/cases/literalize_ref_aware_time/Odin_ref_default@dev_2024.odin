#+feature dynamic-literals
package main

main :: proc() {
shared_time := "12:30:15+02:00"
my_data := map[string]any{
	"x" = shared_time,
}
_ = my_data
}
