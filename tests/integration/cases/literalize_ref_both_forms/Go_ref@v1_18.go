package main

func main() {
SharedValues := []int{
	1,
	2,
}
my_data := map[string][]int{
	"a": SharedValues,
}
my_data = map[string][]int{
	"a": SharedValues,
}
_ = my_data
}
