package main

func main() {
			Shared := []int{
				1,
				2,
			}
			Other := 3
			Payload := "\n    shared : Val\nshared = RInt 99"
			my_data := map[string]any{
				"a": Shared,
				"b": Other,
				"payload": Payload,
			}
_ = my_data
}
