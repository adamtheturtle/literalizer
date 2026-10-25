module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("a-b", OInt 1);
    ("two words", OInt 2);
    ("she said \"hi\"", OInt 3);
    ("", OInt 4);
    ("valid_key", OInt 5)
]

end
