datatype val_t =
    SStr of string
  | SSet of val_t list
val my_data : val_t = SSet [
    SStr "apple",
    SStr "banana",
    SStr "cherry"
]
val _ = my_data
