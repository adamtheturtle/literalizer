package main

func main() {
my_data := map[string]uint64{
	"a": 9223372036854775807,
	"b": uint64(9223372036854775808),
}
_ = my_data
}
