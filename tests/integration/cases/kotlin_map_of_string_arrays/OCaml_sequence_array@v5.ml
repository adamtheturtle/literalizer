module Check = struct

type val_t =
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a", OArray [|OStr "x"|]);
    ("b", OArray [|OStr "y"|])
]

end
