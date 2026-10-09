datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("v", SStr "a\226\128\170\000\195\169\240\159\152\128b")
]
val _ = my_data
