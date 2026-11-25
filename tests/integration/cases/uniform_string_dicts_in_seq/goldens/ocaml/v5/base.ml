module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OMap [("first", OStr "Alice"); ("last", OStr "Smith")];
    OMap [("first", OStr "Bob"); ("last", OStr "Jones")]
]

end
