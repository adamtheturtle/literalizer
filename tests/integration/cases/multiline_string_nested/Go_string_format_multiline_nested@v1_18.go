package main

func main() {
my_data := map[string][][]string{
	`outer`: [][]string{[]string{`nested first line
  indented

nested last line
`}},
}
_ = my_data
}
