datatype val_t =
    SReal of real
  | SList of val_t list
val my_data : val_t = SList [
    SReal 0.0,
    SReal 1.0,
    SReal 1500.0,
    SReal 0.001,
    SReal 1.0E16
]
val _ = my_data
