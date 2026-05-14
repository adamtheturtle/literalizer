package main

func main() {
my_data := map[string]map[string]int{
	"metrics": map[string]int{"count": 100, "rate": 50},
	"flags": map[string]int{"retries": 3, "timeout": 30},
}
_ = my_data
}
