datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val seed : val_t = SInt 1
val my_data : val_t = SList [
    SList [],
    SList [SList []],
    seed
]
val _ = my_data
