type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
  | OSet of val_t list
  | ODate of (int * int * int)
  | ODatetime of ((int * int * int) * (int * int * int))
module Check = struct

let my_data : val_t = OMap [
    ("users", OList [OMap [("name", OStr "Bob"); ("tags", OList [OStr "admin"; OStr "user"])]; OMap [("name", OStr "Carol"); ("tags", OList [OStr "guest"])]])
]

end
