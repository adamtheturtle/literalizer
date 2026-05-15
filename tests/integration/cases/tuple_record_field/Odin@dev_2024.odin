#+feature dynamic-literals
package main

main :: proc() {
my_data := map[string]any{
	"call" = "send",
	"args" = [dynamic]any{1, "email", "a@gmail.com", 100},
}
_ = my_data
}
