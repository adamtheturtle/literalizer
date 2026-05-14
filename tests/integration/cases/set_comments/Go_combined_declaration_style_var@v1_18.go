package main

func main() {
var my_data = map[string]struct{}{
	"apple": struct{}{},  // inline comment
	// before banana
	"banana": struct{}{},
	// trailing
}
my_data = map[string]struct{}{
	"apple": struct{}{},  // inline comment
	// before banana
	"banana": struct{}{},
	// trailing
}
_ = my_data
}
