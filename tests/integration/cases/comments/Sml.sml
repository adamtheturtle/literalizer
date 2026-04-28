datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    (* Server configuration *)
    ("host", SStr "localhost"),  (* default host *)
    ("port", SInt 8080),
    (* Enable debug mode *)
    ("debug", SBool true)
]
val _ = my_data
