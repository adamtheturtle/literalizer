module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [("missing", OInt (-1)); ("present", OInt 1)];
    OMap [("missing", OInt 2); ("present", OInt 3)]
]

end
