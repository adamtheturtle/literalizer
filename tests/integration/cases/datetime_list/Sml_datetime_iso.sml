datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "2024-01-15T12:30:00.123456+00:00",
    SStr "2024-06-01T08:00:00+00:00"
]
val _ = my_data
