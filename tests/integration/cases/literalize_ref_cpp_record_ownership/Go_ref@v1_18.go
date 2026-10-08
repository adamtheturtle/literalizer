package main
type Record1 struct {
	Integer int
	Boolean bool
	Decimal float64
	Null any
}
type Record3 struct {
	Integer int
}
type Record2 struct {
	Child Record3
}
type Record4 struct {
	Text string
}
type Record5 struct {
	Day time.Time
	Stamp time.Time
}
type Record0 struct {
	Trivial Record1
	Nested Record2
	Owning Record4
	Calendar Record5
}
import "time"

func main() {
Trivial := Record1{
	Integer: 1,
	Boolean: true,
	Decimal: 1.5,
	Null: nil,
}
Nested := Record2{
	Child: Record3{
		Integer: 2,
	},
}
Owning := Record4{
	Text: "owned",
}
Calendar := Record5{
	Day: time.Date(2001, time.January, 2, 0, 0, 0, 0, time.UTC),
	Stamp: time.Date(2001, time.January, 2, 3, 4, 5, 0, time.UTC),
}
my_data := Record0{
	Trivial: Trivial,
	Nested: Nested,
	Owning: Owning,
	Calendar: Calendar,
}
_ = my_data
}
