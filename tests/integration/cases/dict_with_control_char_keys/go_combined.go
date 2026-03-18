package main

func main() {
my_data := map[string]any{
    "key\nwith\nnewlines": "value1",
    "key	with	tabs": "value2",
}
my_data = map[string]any{
    "key\nwith\nnewlines": "value1",
    "key	with	tabs": "value2",
}
_ = my_data
}
