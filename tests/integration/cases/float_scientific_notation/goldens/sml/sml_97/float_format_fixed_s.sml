datatype val_t =
    SReal of real
  | SList of val_t list
val my_data : val_t = SList [
    SReal 0.000000,
    SReal 1.000000,
    SReal 1500.000000,
    SReal 0.001000,
    SReal 10000000000000000.000000
]
val _ = my_data
