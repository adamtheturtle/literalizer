package main

func main() {
my_data := map[string]struct{}{
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
