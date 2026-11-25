datatype val_t =
    SInt of LargeInt.int
  | SReal of real
  | SList of val_t list
val integer_value : val_t = SReal 1.0
val my_data : val_t = SList [
    integer_value,
    SReal 1.5
]
val _ = my_data
