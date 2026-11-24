#+feature dynamic-literals
package main

main :: proc() {
my_data := [dynamic]any{
	map[string]any{"call" = "send", "args" = [dynamic]any{1, "email", "a@gmail.com", 100}},
	map[string]any{"call" = "recv", "args" = [dynamic]any{2, "sms", "b@example.com", 200}},
}
_ = my_data
}
