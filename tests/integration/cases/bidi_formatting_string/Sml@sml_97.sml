datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("v", SStr "a\226\128\170\226\128\171\226\128\172\226\128\173\226\128\174\226\129\166\226\129\167\226\129\168\226\129\169b")
]
val _ = my_data
