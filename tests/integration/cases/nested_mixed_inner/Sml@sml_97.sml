datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SList [SInt 1, SStr "a"],
    SList [SInt 2, SStr "b"]
]
val _ = my_data
