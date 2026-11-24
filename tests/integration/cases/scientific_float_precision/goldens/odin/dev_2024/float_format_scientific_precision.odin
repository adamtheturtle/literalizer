#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"value" = 1.2345678901234567,
}
_ = my_data
}
