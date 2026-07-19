package main

func main() {
my_data := map[string]string{
	"x": "\x00",
	"y": "\x001",
}
_ = my_data
}
