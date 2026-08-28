package main

func main() {
	Shared := []int{
		1,
		2,
	}
	my_data := map[string][]int{
		"a": Shared,
	}
_ = my_data
}
