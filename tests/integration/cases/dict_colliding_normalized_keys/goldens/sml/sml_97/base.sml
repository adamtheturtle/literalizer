datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("user_name", SInt 1),
    ("user.name", SInt 2),
    ("user-name", SInt 3),
    ("field_name_that_is_really_quite_long_one", SInt 4),
    ("field_name_that_is_really_quite_long_two", SInt 5)
]
val _ = my_data
