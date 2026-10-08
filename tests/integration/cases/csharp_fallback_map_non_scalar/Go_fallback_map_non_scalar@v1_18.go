package main
type Record0 struct {
	Name string
	Payload map[string]int
}

func main() {
my_data := []Record0{
	Record0{Name: "one", Payload: map[string]int{"scalar": 1, "items": []int{2, 3}}},
	Record0{Name: "two", Payload: map[string]int{"other": 2}},
}
_ = my_data
}
