datatype val_t =
    SStr of string
  | SSet of val_t list
val my_data : val_t = SSet [
    SStr "2024-01-15",
    SStr "2024-06-01"
]
val _ = my_data
