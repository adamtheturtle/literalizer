package main

func main() {
my_data := map[string][]map[string]any{
	"users": []map[string]any{
		{
			"name": "Bob",
			"tags": []string{
				"admin",
				"user",
			},
		},
		{
			"name": "Carol",
			"tags": []string{
				"guest",
			},
		},
	},
}
_ = my_data
}
