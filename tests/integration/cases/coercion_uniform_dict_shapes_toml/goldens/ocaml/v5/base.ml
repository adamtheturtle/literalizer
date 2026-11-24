module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("_", OList [OMap [("type", OStr "create"); ("name", OStr "a")]; OMap [("type", OStr "update"); ("name", OStr "b")]])
]

end
