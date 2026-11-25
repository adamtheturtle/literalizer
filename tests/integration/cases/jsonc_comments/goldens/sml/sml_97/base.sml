datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    (* A JSONC input case with both comment forms. *)
    ("url", SStr "https://example.org/a/*b*/"),  (* detail *)
    (* continued *)
    ("count", SInt 2)  (* trailing line comment *)
]
val _ = my_data
