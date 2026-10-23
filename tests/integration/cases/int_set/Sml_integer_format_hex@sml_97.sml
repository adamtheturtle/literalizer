datatype val_t =
    SInt of LargeInt.int
  | SSet of val_t list
val my_data : val_t = SSet [
    SInt 0x1,
    SInt 0x2,
    SInt 0x3
]
val _ = my_data
