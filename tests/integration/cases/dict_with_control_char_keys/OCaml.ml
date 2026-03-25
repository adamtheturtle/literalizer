module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("key\nwith\nnewlines", OStr "value1");
    ("key\twith\ttabs", OStr "value2");
    ("", OStr "value3")
]

end
