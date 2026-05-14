datatype val_t =
    SReal of real
  | SList of val_t list
val my_data : val_t = SList [
    SReal 1.100000,
    SReal (~2.200000),
    SReal 3.300000
]
val _ = my_data
