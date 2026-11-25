module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OList [OMap [("name", OStr "Alice")]; OMap [("name", OStr "Bob")]];
    OList [OMap [("name", OStr "Charlie")]; OMap [("name", OStr "Dave")]]
]

end
