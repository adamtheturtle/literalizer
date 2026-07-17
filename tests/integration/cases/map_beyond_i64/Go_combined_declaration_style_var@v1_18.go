package main

func main() {
var my_data = map[string]uint64{
	"a": 9223372036854775807,
	"b": uint64(9223372036854775808),
}
my_data = map[string]uint64{
	"a": 9223372036854775807,
	"b": uint64(9223372036854775808),
}
_ = my_data
}
