package main

func main() {
my_data := map[string]struct{}{
	"apple": struct{}{},
	"banana": struct{}{},
	"cherry": struct{}{},
}
my_data = map[string]struct{}{
	"apple": struct{}{},
	"banana": struct{}{},
	"cherry": struct{}{},
}
_ = my_data
}
