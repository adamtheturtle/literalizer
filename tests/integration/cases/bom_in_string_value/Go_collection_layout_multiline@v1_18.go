package main

func main() {
my_data := map[string]string{
	"v": "a\uFEFFb",
}
_ = my_data
}
