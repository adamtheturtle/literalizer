package main
type Record0 struct {
	Name string
	Payload map[string]any
}

func main() {
ZKV := []Record0{
	Record0{
		Name: "ZVal ZKV literalizer record value",
		Payload: map[string]any{
			"scalar": 1,
			"items": map[int]struct{}{
				2: struct{}{},
				3: struct{}{},
			},
		},
	},
	Record0{
		Name: "two",
		Payload: map[string]any{
			"other": 2,
		},
	},
}
_ = ZKV
}
