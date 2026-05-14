datatype val_t =
    SReal of real
  | SList of val_t list
val my_data : val_t = SList [
    SList [SReal 1.500000, SReal 2.500000],
    SList [SReal 3.500000, SReal 4.500000]
]
val _ = my_data
