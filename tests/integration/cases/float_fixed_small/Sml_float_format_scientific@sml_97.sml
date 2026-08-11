datatype val_t =
    SReal of real
  | SList of val_t list
val my_data : val_t = SList [
    SReal 1.0E~9,
    SReal (~1.0E~9)
]
val _ = my_data
