package main

func main() {
MyVar := map[string]string{
	"_": "_",
}
my_data := map[string]map[string]string{
	"key": MyVar,
}
_ = my_data
}
