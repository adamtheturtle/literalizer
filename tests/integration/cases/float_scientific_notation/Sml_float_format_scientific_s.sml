datatype val_t =
    SReal of real
  | SList of val_t list
val my_data : val_t = SList [
    SReal 0.0,
    SReal 1.0,
    SReal 1.5E3,
    SReal 1.0E~3
]
val _ = my_data
