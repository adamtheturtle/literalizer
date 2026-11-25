datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("comma_hash", SStr "a,#b"),
    ("comma_space_hash", SStr "trail, # comment"),
    ("escaped_quote", SStr "quote \" and , #"),
    ("next_line", SStr "x\194\133y"),
    ("line_separator", SStr "x\226\128\168y"),
    ("paragraph_separator", SStr "x\226\128\169y")
]
val _ = my_data
