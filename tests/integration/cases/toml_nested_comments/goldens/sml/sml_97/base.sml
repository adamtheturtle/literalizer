datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    (* About the first dotted key. *)
    (* About the second dotted key. *)
    ("dotted", SMap [("first", SInt 1), ("second", SInt 2)]),
    ("plain", SInt 3),  (* About the plain key. *)
    (* Before the first entry. *)
    (* Before the second entry. *)
    ("entries", SList [SMap [("name", SStr "one")], SMap [("name", SStr "two")]]),
    (* Inside the table. *)
    ("table", SMap [("inner", SInt 4)])
]
val _ = my_data
