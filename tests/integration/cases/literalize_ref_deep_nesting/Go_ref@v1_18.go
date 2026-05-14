package main

func main() {
Deep := map[string]string{
	"_": "_",
}
my_data := map[string]map[string]map[string]map[string]string{
	"a": map[string]map[string]map[string]string{"b": map[string]map[string]string{"c": Deep}},
}
_ = my_data
}
