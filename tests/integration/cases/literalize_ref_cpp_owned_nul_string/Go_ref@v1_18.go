package main

func main() {
Shared := "a\x00b"
my_data := map[string]string{
	"value": Shared,
}
_ = my_data
}
