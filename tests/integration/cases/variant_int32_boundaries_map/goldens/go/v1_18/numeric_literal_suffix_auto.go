package main

func main() {
my_data := map[string]any{
	"below": int64(-2147483649),
	"minimum": int64(-2147483648),
	"above": int64(-2147483647),
	"nested": []int64{int64(0)},
}
_ = my_data
}
