module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let process _ = ()
let my_list : val_t = OMap [
    ("unused", OStr "value")
]
let _ = process(OList [OList [OMap [("inner", my_list)]]])

end
