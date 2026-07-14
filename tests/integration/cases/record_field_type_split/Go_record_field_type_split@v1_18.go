package main
type Record1 struct {
	Status int
}
type Record2 struct {
	Status string
}
type Record4 struct {
	Kind string
	Urgent bool
}
type Record3 struct {
	Inner Record4
}
type Record6 struct {
	Error string
}
type Record5 struct {
	Inner Record6
}
type Record7 struct {
	Holder Record1
}
type Record8 struct {
	Holder Record2
}
type Record9 struct {
	Nums []int
}
type Record0 struct {
	Plain Record1
	Other Record2
	NestedA Record3
	NestedB Record5
	WrapA Record7
	WrapB Record8
	Wide Record9
}

func main() {
my_data := Record0{
	Plain: Record1{
		Status: 1,
	},
	Other: Record2{
		Status: "ready",
	},
	NestedA: Record3{
		Inner: Record4{
			Kind: "add",
			Urgent: true,
		},
	},
	NestedB: Record5{
		Inner: Record6{
			Error: "not_found",
		},
	},
	WrapA: Record7{
		Holder: Record1{
			Status: 2,
		},
	},
	WrapB: Record8{
		Holder: Record2{
			Status: "word",
		},
	},
	Wide: Record9{
		Nums: []int{
			1,
			1099511627776,
		},
	},
}
_ = my_data
}
