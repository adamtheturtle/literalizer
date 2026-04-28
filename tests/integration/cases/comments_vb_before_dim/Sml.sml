datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    (* Configuration *)
    ("name", SStr "app"),
    (* Port setting *)
    ("port", SInt 3000)
]
val _ = my_data
