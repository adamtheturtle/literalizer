datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SMap [
        (* inner note *)
        ("b", SInt 1)  (* inline b *)
    ]),
    ("list", SList [
        SInt 1,  (* first *)
        SInt 2  (* second *)
    ])
]
val _ = my_data
