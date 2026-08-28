datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SMap [
        ("b", SList [SInt 1]),
        (* Outdented from the sequence, so the inner mapping claims this. *)
        ("c", SInt 2)
    ]),
    (* Outdented from the inner mapping too, so the root claims this. *)
    ("d", SInt 3)
]
val _ = my_data
