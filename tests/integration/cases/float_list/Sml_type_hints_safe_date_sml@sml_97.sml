datatype val_t =
    SReal of real
  | SList of val_t list
val my_data : val_t = SList [
    SReal 1.1,
    SReal (~2.2),
    SReal 3.3
]
val _ = my_data
