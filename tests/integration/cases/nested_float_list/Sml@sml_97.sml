datatype val_t =
    SReal of real
  | SList of val_t list
val my_data : val_t = SList [
    SList [SReal 1.5, SReal 2.5],
    SList [SReal 3.5, SReal 4.5]
]
val _ = my_data
