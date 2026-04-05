#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]struct{}{
	"2024-01-15" = {},
	"2024-06-01" = {},
}
_ = my_data
}
