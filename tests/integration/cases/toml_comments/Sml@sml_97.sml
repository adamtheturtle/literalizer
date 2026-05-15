datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    (* before *)
    ("answer", SInt 42),  (* inline *)
    ("plain", SStr "ok")
    (* trailing *)
]
val _ = my_data
