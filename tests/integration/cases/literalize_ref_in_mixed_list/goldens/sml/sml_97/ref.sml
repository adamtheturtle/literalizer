datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val ref_x : val_t = SInt 3
val my_data : val_t = SList [
    ref_x,
    SInt 1,
    SInt 2
]
val _ = my_data
