datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SList [
        SMap [("item", SStr "existing")],
        SStr "kept"
        (* This comment trails the first pair. *)
    ],
    SList [SMap [("item", SStr "next")], SStr "also kept"],
    (* This comment describes the last pair. *)
    SList [SMap [("item", SStr "last")], SStr "kept too"]
]
val _ = my_data
