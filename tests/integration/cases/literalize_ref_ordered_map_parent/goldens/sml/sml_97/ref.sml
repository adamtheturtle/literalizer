datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val bound : val_t = SInt 2
val my_data : val_t = SMap [
    ("value", bound)
]
val _ = my_data
