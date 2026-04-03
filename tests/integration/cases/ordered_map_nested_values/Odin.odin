package main

main :: proc() {
my_data := map[string]any{
	"name" = "Alice",
	"scores" = map[string]any{"1" = "first", "2" = "second"},
}
_ = my_data
}
