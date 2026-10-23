package main

func main() {
my_data := map[string]string{
	"v": "a‪\x00é😀b",
}
_ = my_data
}
