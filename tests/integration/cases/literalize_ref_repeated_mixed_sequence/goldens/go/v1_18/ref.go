package main

func main() {
Shared := []any{
	1,
	"x",
}
my_data := []any{
	Shared,
	Shared,
}
_ = my_data
}
