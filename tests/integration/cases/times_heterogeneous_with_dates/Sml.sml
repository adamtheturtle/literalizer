datatype val_t =
    SStr of string
  | SDate of (int * int * int)
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("vals", SList [SDate (2024, 1, 15), "09:30:00"])
]
val _ = my_data
