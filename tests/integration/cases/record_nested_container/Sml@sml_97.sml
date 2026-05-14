datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("title", SStr "report"),
    ("tags", SList [SStr "draft", SStr "urgent", SStr "review"]),
    ("priority", SInt 2)
]
val _ = my_data
