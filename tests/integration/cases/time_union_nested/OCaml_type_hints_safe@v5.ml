module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("mixed", OList [OList [OStr "09:30:00"]; OList []])
]

end
