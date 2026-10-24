#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]struct{}{
	"2099-06-15T08:30:00" = {},
}
_ = my_data
}
