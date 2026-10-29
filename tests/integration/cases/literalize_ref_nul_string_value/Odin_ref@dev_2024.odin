#+feature dynamic-literals
package main

main :: proc() {
shared := "a\x00b"
my_data := map[string]any{
	"value" = shared,
}
_ = my_data
}
