datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("first", SList [
        SInt 1,
        SInt 2
    ]),
    ("second", SInt 3)  (* About the second key. *)
]
val _ = my_data
