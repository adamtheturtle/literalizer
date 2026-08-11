datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val foo : val_t = SMap [
    ("_", SStr "_")
]
val my_data : val_t = SMap [
    ("mapping", SMap [("value", foo)]),
    ("items", SList [SMap [("other", SInt 1)], foo])
]
val _ = my_data
