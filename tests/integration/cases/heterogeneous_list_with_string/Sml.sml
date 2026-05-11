datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "hello",
    SInt 42
]
val _ = my_data
