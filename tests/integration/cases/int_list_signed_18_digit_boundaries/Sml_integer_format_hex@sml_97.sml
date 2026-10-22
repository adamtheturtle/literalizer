datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val my_data : val_t = SList [
    SInt 0xde0b6b3a763ffff,
    SInt (~0xde0b6b3a763ffff)
]
val _ = my_data
