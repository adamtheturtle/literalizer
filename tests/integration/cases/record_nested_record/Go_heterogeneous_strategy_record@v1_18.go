package main
type Record1 struct {
	Name string
	Age int
}
type Record0 struct {
	Id int
	Owner Record1
}

func main() {
my_data := Record0{
	Id: 1,
	Owner: Record1{
		Name: "Alice",
		Age: 30,
	},
}
_ = my_data
}
