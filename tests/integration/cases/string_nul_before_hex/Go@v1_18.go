package main

func main() {
my_data := map[string]string{
	"x": "before\x00after",
}
_ = my_data
}
