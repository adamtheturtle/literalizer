datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val my_data : val_t = SList [
    SInt 1000000,
    SInt (~1234),
    SInt 255,
    SInt (~10)
]
val _ = my_data
