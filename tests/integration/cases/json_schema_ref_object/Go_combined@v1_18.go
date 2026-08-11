package main

func main() {
my_data := map[string]map[string]string{
	"schema": map[string]string{"$ref": "#/defs/Foo"},
}
my_data = map[string]map[string]string{
	"schema": map[string]string{"$ref": "#/defs/Foo"},
}
_ = my_data
}
