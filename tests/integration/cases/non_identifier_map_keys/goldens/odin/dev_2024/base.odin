#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"a-b" = 1,
	"two words" = 2,
	"she said \"hi\"" = 3,
	"" = 4,
	"valid_key" = 5,
}
_ = my_data
}
