package main

func main() {
my_data := []map[string]any{
	{"call": "send", "args": []any{1, "email", "a@gmail.com", 100}},
	{"call": "recv", "args": []any{2, "sms", "b@example.com", 200}},
}
_ = my_data
}
