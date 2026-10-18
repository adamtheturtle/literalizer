datatype val_t =
    SInt of LargeInt.int
  | SSet of val_t list
val my_data : val_t = SSet [
    SInt (~2147483649),
    SInt (~2147483648),
    SInt 2147483647,
    SInt 2147483648
]
val _ = my_data
