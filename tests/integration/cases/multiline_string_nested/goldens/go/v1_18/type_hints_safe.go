package main

func main() {
my_data := map[string][][]string{
	"outer": [][]string{[]string{"nested first line\n  indented\n\nnested last line\n"}},
}
_ = my_data
}
