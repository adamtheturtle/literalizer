datatype val_t =
    SStr of string
  | SSet of val_t list
val my_data : val_t = SSet [
    SStr "1969-12-31T23:59:59+00:00"
]
val _ = my_data
