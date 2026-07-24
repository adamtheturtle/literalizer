module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [("id", OInt 100); ("label", OStr "first entry"); ("enabled", OBool false); ("related_ids", OList [OInt 102; OInt 103])];
    OMap [("id", OInt 101); ("label", OStr "second entry"); ("enabled", OBool true); ("related_ids", OList [OInt 100])]
]

end
