package main

func main() {
Shared := []int{
	1,
	2,
}
Second := "two"
my_data := []any{
	Shared,
	Second,
}
my_data = []any{
	Shared,
	Second,
}
_ = my_data
}
