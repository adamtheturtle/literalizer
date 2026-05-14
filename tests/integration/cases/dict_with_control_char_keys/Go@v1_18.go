package main

func main() {
my_data := map[string]string{
	"key\nwith\nnewlines": "value1",
	"key\twith\ttabs": "value2",
	"": "value3",
}
_ = my_data
}
