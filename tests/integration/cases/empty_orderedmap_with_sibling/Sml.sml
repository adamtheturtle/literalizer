datatype val_t =
    SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [],
    SList []
]
val _ = my_data
