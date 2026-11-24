datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("level1", SMap [("level2", SMap [("level3", SMap [("level4", SMap [("value", SStr "deep"), ("items", SList [SStr "a", SStr "b"])])]), ("sibling", SInt 42)]), ("tags", SList [SMap [("name", SStr "tag1"), ("meta", SMap [("priority", SInt 1), ("labels", SList [SStr "x", SStr "y"])])]])])
]
val _ = my_data
