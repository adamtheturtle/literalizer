datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SInt 0,
    SList [SList [SStr "plain"]]
]
val _ = my_data
