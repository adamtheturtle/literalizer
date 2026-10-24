module Check = struct

type val_t =
  | OStr of string
  | ODate of (int * int * int)
  | OInt of int
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("date", ODate (99, 5, 27));
    ("naive", OInt (-62135551800));
    ("recent", OInt 1716804000)
]

end
