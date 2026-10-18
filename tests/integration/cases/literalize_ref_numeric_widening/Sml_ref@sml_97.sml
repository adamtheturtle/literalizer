datatype val_t =
    SInt of LargeInt.int
  | SReal of real
  | SList of val_t list
val floating_value : val_t = SReal 1.5
val integer_value : val_t = SReal 2.0
val my_data : val_t = SList [
    floating_value,
    integer_value
]
val _ = my_data
