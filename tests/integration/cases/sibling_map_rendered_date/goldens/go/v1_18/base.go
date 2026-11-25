package main
import "time"

func main() {
my_data := map[string]map[string]any{
	"a": map[string]any{"k": time.Date(2020, time.January, 1, 0, 0, 0, 0, time.UTC)},
	"b": map[string]any{"k": "string"},
}
_ = my_data
}
