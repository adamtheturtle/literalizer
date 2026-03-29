module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("name", OStr "Alice");
    ("scores", OMap [("1", OStr "first"); ("2", OStr "second")])
]

end
