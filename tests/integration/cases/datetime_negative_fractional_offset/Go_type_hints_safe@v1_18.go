package main
import "time"

func main() {
my_data := time.Date(2000, time.January, 1, 0, 0, 0, 0, time.FixedZone("", -19800))
_ = my_data
}
