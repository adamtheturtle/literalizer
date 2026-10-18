datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SList [SInt 1, SStr "two"],
    SList []
]
val _ = my_data
