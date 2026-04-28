datatype val_t =
    SDate of (int * int * int)
  | SList of val_t list
val my_data : val_t = SList [
    SDate (2024, 1, 15),
    SDate (2024, 2, 20)
]
val _ = my_data
