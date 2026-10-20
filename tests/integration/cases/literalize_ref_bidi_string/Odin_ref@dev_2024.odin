#+feature dynamic-literals
package main

main :: proc() {
text := "a‪b"
my_data := map[string]any{
	"value" = text,
}
_ = my_data
}
