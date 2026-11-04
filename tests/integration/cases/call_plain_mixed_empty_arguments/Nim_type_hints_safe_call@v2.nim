proc make_widget[T0, T1, T2](before: T0; populated: T1; after: T2): int {.discardable.} = 0
proc make_widget[T1](before: array[0, int]; populated: T1; after: array[0, int]): int {.discardable.} = 0
proc make_widget[T0, T1](before: T0; populated: T1; after: array[0, int]): int {.discardable.} = 0
make_widget([], [1], [])
make_widget(["text"], [2], [])
make_widget([], ["text"], [])
make_widget(["text"], [2], [3])
