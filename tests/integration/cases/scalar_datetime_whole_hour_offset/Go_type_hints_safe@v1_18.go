package main
import "time"

func main() {
my_data := time.Date(2024, time.January, 15, 18, 0, 0, 0, time.FixedZone("", 18000))
_ = my_data
}
