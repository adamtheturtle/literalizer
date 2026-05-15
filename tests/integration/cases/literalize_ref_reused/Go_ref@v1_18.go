package main

func main() {
SharedVar := map[string]string{
	"_": "_",
}
my_data := []map[string]string{
	SharedVar,
	SharedVar,
}
_ = my_data
}
