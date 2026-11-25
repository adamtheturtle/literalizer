datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val my_data : val_t = SList [
    SInt (~9223372036854775808),
    SInt (~1),
    SInt 9223372036854775807
]
val _ = my_data
