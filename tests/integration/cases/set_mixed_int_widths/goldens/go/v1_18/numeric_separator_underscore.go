package main

func main() {
my_data := map[int64]struct{}{
	1: struct{}{},
	1_099_511_627_776: struct{}{},
}
_ = my_data
}
