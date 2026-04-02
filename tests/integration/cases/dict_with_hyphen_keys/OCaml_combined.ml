module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("my-key", OStr "value1");
    ("another-key", OStr "value2");
    ("normal_key", OStr "value3")
]

end
