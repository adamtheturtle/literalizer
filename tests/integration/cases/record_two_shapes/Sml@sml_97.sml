datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("user", SMap [("id", SInt 1), ("name", SStr "Alice")]),
    ("project", SMap [("title", SStr "report"), ("tags", SList [SStr "draft", SStr "urgent"])])
]
val _ = my_data
