#+feature dynamic-literals
package main
Record0 :: struct { call: string, args: [dynamic]any }

main :: proc() {
my_data := [dynamic]any{
	Record0{ call = "send", args = [dynamic]any{1, "email", "a@gmail.com", 100} },
	Record0{ call = "recv", args = [dynamic]any{2, "sms", "b@example.com", 200} },
}
_ = my_data
}
