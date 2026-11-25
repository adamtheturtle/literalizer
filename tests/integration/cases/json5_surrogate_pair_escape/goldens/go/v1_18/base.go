package main

func main() {
my_data := map[string]any{
	"astral": "😀",
	"mixed": "a😀b",
	"count": 2,
	"list": []any{"😀", 1},
	"nested": map[string]string{"inner": "😀"},
}
_ = my_data
}
