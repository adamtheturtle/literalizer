datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val my_data : val_t = SList [
    SInt 0,
    SInt 1,
    SInt (~1)
]
val _ = my_data
