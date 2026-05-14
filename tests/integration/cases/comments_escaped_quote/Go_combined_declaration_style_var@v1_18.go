package main

func main() {
var my_data = map[string]string{
	"key": "value \" # not a comment",  // real
}
my_data = map[string]string{
	"key": "value \" # not a comment",  // real
}
_ = my_data
}
