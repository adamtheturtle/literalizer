package main
type Record1 struct {
	Kind string
	Urgent bool
}
type Record0 struct {
	Entries []Record1
}
type Record3 struct {
	Error string
}
type Record2 struct {
	Entries []Record3
}

func main() {
my_data := [][2]any{
	{"left", Record0{Entries: []Record1{Record1{Kind: "add", Urgent: true}}}},
	{"right", Record2{Entries: []Record3{Record3{Error: "not_found"}}}},
}
_ = my_data
}
