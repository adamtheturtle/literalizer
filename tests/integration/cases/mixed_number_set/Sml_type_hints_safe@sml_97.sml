datatype val_t =
    SInt of LargeInt.int
  | SReal of real
  | SSet of val_t list
val my_data : val_t = SSet [
    SReal 2.5,
    SInt 1
]
val _ = my_data
