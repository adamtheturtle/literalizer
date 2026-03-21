package main
import "time"

func main() {
my_data := []any{
    time.Date(2024, time.January, 15, 12, 30, 0, 0, time.UTC),
    time.Date(2024, time.June, 30, 8, 0, 0, 0, time.UTC),
    time.Date(2024, time.December, 25, 18, 45, 0, 0, time.UTC),
}
my_data = []any{
    time.Date(2024, time.January, 15, 12, 30, 0, 0, time.UTC),
    time.Date(2024, time.June, 30, 8, 0, 0, 0, time.UTC),
    time.Date(2024, time.December, 25, 18, 45, 0, 0, time.UTC),
}
_ = my_data
}
