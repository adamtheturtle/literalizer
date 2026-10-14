package main

func main() {
my_data := map[string]struct{}{
	"1901-12-13T20:45:51": struct{}{},
	"1901-12-13T20:45:52": struct{}{},
	"2038-01-19T03:14:07": struct{}{},
	"2038-01-19T03:14:08": struct{}{},
}
_ = my_data
}
