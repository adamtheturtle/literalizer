datatype val_t =
    SInt of LargeInt.int
  | SSet of val_t list
val my_data : val_t = SSet [
    SInt 1,
    SInt 1099511627776
]
val _ = my_data
