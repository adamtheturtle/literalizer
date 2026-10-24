package main
import "time"

func main() {
my_data := map[string]map[string]any{
	"b": map[string]any{"k": 1},
	"a": map[string]any{"k": time.Date(2040, time.January, 1, 0, 0, 0, 0, time.UTC)},
}
_ = my_data
}
