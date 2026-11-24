package main

func main() {
my_data := map[string]uint64{
	"a": 9_223_372_036_854_775_807,
	"b": uint64(9223372036854775808),
}
_ = my_data
}
