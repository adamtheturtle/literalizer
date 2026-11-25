datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("call", SStr "send"), ("args", SList [SInt 1, SStr "email", SStr "a@gmail.com", SInt 100])],
    SMap [("call", SStr "recv"), ("args", SList [SInt 2, SStr "sms", SStr "b@example.com", SInt 200])]
]
val _ = my_data
