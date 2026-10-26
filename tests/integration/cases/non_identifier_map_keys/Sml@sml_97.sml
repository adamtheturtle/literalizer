datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a-b", SInt 1),
    ("two words", SInt 2),
    ("she said \"hi\"", SInt 3),
    ("", SInt 4),
    ("valid_key", SInt 5)
]
val _ = my_data
