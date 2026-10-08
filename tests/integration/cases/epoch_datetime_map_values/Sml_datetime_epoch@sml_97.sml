datatype val_t =
    SStr of string
  | SInt of LargeInt.int
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("within_i32", SInt 1705320000),
    ("beyond_i32", SInt 4085195400)
]
val _ = my_data
