module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [("id", OInt 100); ("description", OStr "first task"); ("is_done", OBool false); ("blocks", OList [OInt 102; OInt 103])];
    OMap [("id", OInt 101); ("description", OStr "second task"); ("is_done", OBool true); ("blocks", OList [])]
]

end
