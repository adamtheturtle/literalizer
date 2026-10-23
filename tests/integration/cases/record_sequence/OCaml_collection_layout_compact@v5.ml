module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [("id", OInt 1); ("label", OStr "first"); ("tags", OList [])];
    OMap [("id", OInt 2); ("label", OStr "second"); ("tags", OList [])];
    OMap [("id", OInt 3); ("label", OStr "third"); ("tags", OList [])]
]

end
