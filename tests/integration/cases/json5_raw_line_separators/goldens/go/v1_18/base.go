package main

func main() {
my_data := map[string]string{
	"double": "a b",
	"single": "c d",
	// A comment, which both separators would end.
	"both": "e f g",
	"continued": "hi",
	"escaped backslash": "j\\ k",
}
_ = my_data
}
