package main

func main() {
my_data := map[string]any{
	// About the first dotted key.
	// About the second dotted key.
	"dotted": map[string]int{"first": 1, "second": 2},
	"plain": 3,  // About the plain key.
	// Before the first entry.
	// Before the second entry.
	"entries": []map[string]string{{"name": "one"}, {"name": "two"}},
	// Inside the table.
	"table": map[string]int{"inner": 4},
}
_ = my_data
}
