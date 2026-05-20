module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [("item", OStr "existing")];
    (* This comment describes the next item. *)
    OMap [("item", OStr "next")]
]

end
