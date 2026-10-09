package main
type Record1 struct {
	X int
	Y any
}
type Record2 struct {
	X any
	Y any
}
type Record3 struct {
	X int
	Y int
}
type Record0 struct {
	Nullable Record1
	NullFields Record2
	Plain Record3
}

func main() {
Nullable := Record1{
	X: 1,
	Y: nil,
}
NullFields := Record2{
	X: nil,
	Y: nil,
}
Plain := Record3{
	X: 1,
	Y: 2,
}
my_data := Record0{
	Nullable: Nullable,
	NullFields: NullFields,
	Plain: Plain,
}
_ = my_data
}
