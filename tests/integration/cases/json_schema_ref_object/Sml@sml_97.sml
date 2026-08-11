datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("schema", SMap [("$ref", SStr "#/defs/Foo")])
]
val _ = my_data
