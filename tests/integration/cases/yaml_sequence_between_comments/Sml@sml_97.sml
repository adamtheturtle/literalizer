datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("item", SStr "existing")],
    (* This comment describes the next item. *)
    SMap [("item", SStr "next")]
]
val _ = my_data
