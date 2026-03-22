package main

var _ = map[any]struct{}{
    // before apple
    "apple": struct{}{},
    "banana": struct{}{},  // banana inline
    // trailing
}
