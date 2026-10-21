datatype val_t =
    SDate of (int * int * int)
  | SSet of val_t list
val my_data : val_t = SSet [
    SDate (2024, 1, 15),
    SDate (2024, 6, 1)
]
val _ = my_data
