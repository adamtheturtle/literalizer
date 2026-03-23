package main

func main() {
my_data := map[any]struct{}{
    1: struct{}{},
    2: struct{}{},
    3: struct{}{},
}
my_data = map[any]struct{}{
    1: struct{}{},
    2: struct{}{},
    3: struct{}{},
}
_ = my_data
}
