package main

var _ = map[any]struct{}{
    true: struct{}{},
    42: struct{}{},
    "apple": struct{}{},
}
