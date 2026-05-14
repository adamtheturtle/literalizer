#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"morning" = "09:30:00",
	"afternoon" = "14:15:00",
	"evening" = "23:59:59",
}
_ = my_data
}
