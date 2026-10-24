datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SList [],
    SList [SInt 1, SStr "value"],
    SList [SInt 2, SInt 3]
]
val _ = my_data
