module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OList [
        OMap [("item", OStr "existing")];
        OStr "kept"
        (* This comment trails the first pair. *)
    ];
    OList [OMap [("item", OStr "next")]; OStr "also kept"];
    (* This comment describes the last pair. *)
    OList [OMap [("item", OStr "last")]; OStr "kept too"]
]

end
