datatype val_t =
    SReal of real
  | SList of val_t list
val my_data : val_t = SList [
    SReal (~0.000000),
    SReal 1.500000
]
val _ = my_data
