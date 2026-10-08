datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val existing : val_t = SInt 1
val my_data : val_t = SList [
    SInt 0,
    SList [SList [existing]]
]
val _ = my_data
