package main

func main() {
var my_data = map[string]string{
	"key\nwith\nnewlines": "value1",
	"key\twith\ttabs": "value2",
	"": "value3",
}
my_data = map[string]string{
	"key\nwith\nnewlines": "value1",
	"key\twith\ttabs": "value2",
	"": "value3",
}
_ = my_data
}
