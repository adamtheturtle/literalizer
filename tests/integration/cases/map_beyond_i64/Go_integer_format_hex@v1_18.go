package main

func main() {
my_data := map[string]uint64{
	"a": 0x7fffffffffffffff,
	"b": uint64(9223372036854775808),
}
_ = my_data
}
