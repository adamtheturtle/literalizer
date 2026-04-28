datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val my_data : val_t = SList [
    SInt 0x0,
    SInt 0x1,
    SInt (~0x1)
]
val _ = my_data
