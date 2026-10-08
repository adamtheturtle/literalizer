datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val my_data : val_t = SList [
    SList [SInt 1, SList []],
    SList [SInt 2, SList [SInt 3]]
]
val _ = my_data
