package main

func main() {
my_data := map[string]string{
	// heading
	"a": "single ' // data",
	"b": "linecontinuation",
	"c": "\\",  // actual comment
	"d": "  ",  // final comment
}
_ = my_data
}
