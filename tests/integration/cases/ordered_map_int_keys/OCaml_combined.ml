module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("1", OStr "one");
    ("2", OStr "two");
    ("42", OStr "answer")
]

end
