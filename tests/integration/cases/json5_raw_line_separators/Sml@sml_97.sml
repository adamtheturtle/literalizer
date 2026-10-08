datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("double", SStr "a\226\128\168b"),
    ("single", SStr "c\226\128\169d"),
    ("both", SStr "e\226\128\168f\226\128\169g"),
    ("continued", SStr "hi"),
    ("escaped backslash", SStr "j\\\226\128\168k")
]
val _ = my_data
