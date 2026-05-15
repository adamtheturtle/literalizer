package main
type Record1 struct {
	Count int
	Rate int
}
type Record2 struct {
	Retries int
	Timeout int
}
type Record0 struct {
	Metrics Record1
	Flags Record2
}

func main() {
my_data := Record0{
	Metrics: Record1{
		Count: 100,
		Rate: 50,
	},
	Flags: Record2{
		Retries: 3,
		Timeout: 30,
	},
}
_ = my_data
}
