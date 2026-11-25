datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("collection", SStr "alpha"),
    ("featured_entry", SMap [("id", SInt 100), ("label", SStr "first entry"), ("enabled", SBool false), ("related_ids", SList [SInt 102, SInt 103])])
]
val _ = my_data
