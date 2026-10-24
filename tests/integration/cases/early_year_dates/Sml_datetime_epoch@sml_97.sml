datatype val_t =
    SStr of string
  | SDate of (int * int * int)
  | SInt of LargeInt.int
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("date", SDate (99, 5, 27)),
    ("naive", SInt (~62135551800)),
    ("recent", SInt 1716804000)
]
val _ = my_data
