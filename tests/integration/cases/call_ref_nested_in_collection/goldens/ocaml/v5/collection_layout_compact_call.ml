module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let process _ = ()
let big_list : val_t = OList [
    OStr "x"
]
let _ = process(OMap [("k", big_list)], OInt 2)

end
