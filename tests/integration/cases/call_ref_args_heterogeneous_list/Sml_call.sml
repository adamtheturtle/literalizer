datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
fun process _ = ()
val my_ints : val_t = SList [
    SInt 1,
    SInt 2,
    SInt 3
]
val my_strings : val_t = SList [
    SStr "a",
    SStr "b"
]
val my_empty : val_t = SList []
val _ = process(my_ints, 42)
val _ = process(my_strings, 7)
val _ = process(my_empty, 99)
