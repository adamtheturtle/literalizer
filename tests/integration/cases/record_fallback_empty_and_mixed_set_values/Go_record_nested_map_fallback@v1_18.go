package main
type Record0 struct {
	Name string
	Payload map[string]any
}

func main() {
my_data := []Record0{
	Record0{Name: "one", Payload: map[string]any{"scalar": 1, "empty": map[any]struct{}{}, "mixed": map[any]struct{}{2: struct{}{}, "word": struct{}{}}}},
	Record0{Name: "two", Payload: map[string]any{"other": 2}},
}
_ = my_data
}
