datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val whole : val_t = SList [
    SInt 1,
    SInt 2
]
val my_data : val_t = whole
val _ = my_data
