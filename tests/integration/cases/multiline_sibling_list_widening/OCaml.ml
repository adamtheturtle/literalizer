module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("sibling_lists", OMap [("numbers", OList [OInt 1; OInt 2]); ("strings", OList [OStr "x"; OStr "y"])]);
    ("ref_marker_present", OList [OStr "$keep"; OStr "z"])
]

end
