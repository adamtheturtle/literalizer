datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "1970-01-01T00:00:00.000001+00:00",
    SStr "1969-12-31T23:59:59.500000+00:00",
    SStr "1970-01-01T00:00:01+00:00"
]
val _ = my_data
