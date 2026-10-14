datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val my_data : val_t = SList [
    SInt (~0x80000000),
    SInt (~0x7fffffff),
    SList [SInt 0x0]
]
val _ = my_data
