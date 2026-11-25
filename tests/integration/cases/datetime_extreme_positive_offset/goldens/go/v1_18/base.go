package main
import "time"

func main() {
my_data := time.Date(2020, time.June, 15, 12, 0, 0, 0, time.FixedZone("", 86340))
_ = my_data
}
