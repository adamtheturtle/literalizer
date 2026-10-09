package main

func main() {
my_data := [][2]any{
	{`  leading
key  `, `  leading
value
  `},
	{`next
	key`, []string{`
first
`, ` last
 `}},
}
_ = my_data
}
