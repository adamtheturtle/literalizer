module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("id", OInt 1);
    ("label", OStr "She said \"hello\", then waved");
    ("enabled", OBool false);
    ("related_ids", OList [OInt 1; OInt 2; OInt 3])
]

end
