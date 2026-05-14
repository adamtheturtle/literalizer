datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("users", SList [SMap [("name", SStr "Bob"), ("tags", SList [SStr "admin", SStr "user"])], SMap [("name", SStr "Carol"), ("tags", SList [SStr "guest"])]])
]
val _ = my_data
