module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("astral", OStr "😀");
    ("mixed", OStr "a😀b");
    ("count", OInt 2);
    ("list", OList [OStr "😀"; OInt 1]);
    ("nested", OMap [("inner", OStr "😀")])
]

end
