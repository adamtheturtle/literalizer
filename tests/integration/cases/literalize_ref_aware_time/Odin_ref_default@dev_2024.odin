#+feature dynamic-literals
package main

main :: proc() {
value := "12:30:15+02:00"
my_data := map[string]any{
	"x" = value,
}
_ = my_data
}
