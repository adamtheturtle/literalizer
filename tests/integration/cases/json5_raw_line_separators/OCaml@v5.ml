module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("double", OStr "a b");
    ("single", OStr "c d");
    ("both", OStr "e f g");
    ("continued", OStr "hi");
    ("escaped backslash", OStr "j\\ k")
]

end
