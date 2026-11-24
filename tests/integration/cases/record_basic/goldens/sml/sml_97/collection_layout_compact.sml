datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("id", SInt 1),
    ("label", SStr "She said \"hello\", then waved"),
    ("enabled", SBool false),
    ("related_ids", SList [SInt 1, SInt 2, SInt 3])
]
val _ = my_data
