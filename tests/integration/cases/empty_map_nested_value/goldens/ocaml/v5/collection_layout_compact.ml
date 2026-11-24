module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OList [OMap [("mapping", OMap [])]; OMap []];
    OList [OMap []; OMap [("mapping", OMap [])]]
]

end
