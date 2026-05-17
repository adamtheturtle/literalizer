#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"starts_at" = "09:30:00",
}
_ = my_data
}
