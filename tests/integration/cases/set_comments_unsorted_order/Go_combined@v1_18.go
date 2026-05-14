package main

func main() {
my_data := map[string]struct{}{
	// before apple
	"apple": struct{}{},
	"banana": struct{}{},  // banana inline
	// trailing
}
my_data = map[string]struct{}{
	// before apple
	"apple": struct{}{},
	"banana": struct{}{},  // banana inline
	// trailing
}
_ = my_data
}
