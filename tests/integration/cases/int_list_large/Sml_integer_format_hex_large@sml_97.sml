datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val my_data : val_t = SList [
    SInt 0xf4240,
    SInt (~0x4d2),
    SInt 0xff,
    SInt (~0xa)
]
val _ = my_data
