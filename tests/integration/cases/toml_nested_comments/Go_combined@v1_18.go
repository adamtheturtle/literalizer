package main

func main() {
my_data := map[string]any{
	// About the first dotted key.
	// About the second dotted key.
	"dotted": map[string]int{"first": 1, "second": 2},
	"plain": 3,  // About the plain key.
	// Inside the table.
	"table": map[string]int{"inner": 4},
	// Before the first entry.
	// Before the second entry.
	"entries": []map[string]string{{"name": "one"}, {"name": "two"}},
}
my_data = map[string]any{
	// About the first dotted key.
	// About the second dotted key.
	"dotted": map[string]int{"first": 1, "second": 2},
	"plain": 3,  // About the plain key.
	// Inside the table.
	"table": map[string]int{"inner": 4},
	// Before the first entry.
	// Before the second entry.
	"entries": []map[string]string{{"name": "one"}, {"name": "two"}},
}
_ = my_data
}
