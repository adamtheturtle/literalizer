datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("flow", SList [
        SInt 1,
        (* After the first element. *)
        SInt 2
    ]),
    (* Between the key and its value. *)
    ("gap", SInt 3),
    (* On the block scalar header. *)
    ("block", SStr "Text.\n"),
    ("anchored", SInt 4),
    ("alias", SInt 4)
    (* On the alias. *)
]
val _ = my_data
