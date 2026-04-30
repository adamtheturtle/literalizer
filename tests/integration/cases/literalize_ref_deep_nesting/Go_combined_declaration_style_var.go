package main

func main() {
var my_data = map[string]map[string]map[string]map[string]string{
	"a": map[string]map[string]map[string]string{"b": map[string]map[string]string{"c": map[string]string{"$ref": "deep"}}},
}
my_data = map[string]map[string]map[string]map[string]string{
	"a": map[string]map[string]map[string]string{"b": map[string]map[string]string{"c": map[string]string{"$ref": "deep"}}},
}
_ = my_data
}
