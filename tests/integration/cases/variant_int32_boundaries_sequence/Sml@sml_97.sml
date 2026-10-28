datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val my_data : val_t = SList [
    SInt (~2147483648),
    SInt (~2147483647),
    SList [SInt 0]
]
val _ = my_data
