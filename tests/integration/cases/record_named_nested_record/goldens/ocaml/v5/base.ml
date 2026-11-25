module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("collection", OStr "alpha");
    ("featured_entry", OMap [("id", OInt 100); ("label", OStr "first entry"); ("enabled", OBool false); ("related_ids", OList [OInt 102; OInt 103])])
]

end
