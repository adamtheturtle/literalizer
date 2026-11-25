datatype val_t =
    SStr of string
  | SSet of val_t list
val my_data : val_t = SSet [
    SStr "2099-06-15T08:30:00"
]
val _ = my_data
