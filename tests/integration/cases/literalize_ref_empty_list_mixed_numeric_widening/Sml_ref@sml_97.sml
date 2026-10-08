datatype val_t =
    SInt of LargeInt.int
  | SReal of real
  | SList of val_t list
val empty_values : val_t = SList []
val integer_values : val_t = SList [
    SInt 1
]
val float_values : val_t = SList [
    SReal 1.5
]
val my_data : val_t = SList [
    empty_values,
    integer_values,
    float_values
]
val _ = my_data
