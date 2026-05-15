package main
type Record0 struct {
	Call string
	Args []any
}

func main() {
my_data := []any{
	Record0{Call: "send", Args: []any{1, "email", "a@gmail.com", 100}},
	Record0{Call: "recv", Args: []any{2, "sms", "b@example.com", 200}},
}
_ = my_data
}
