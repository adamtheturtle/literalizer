module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    (* Configuration *)
    ("name", OStr "app");
    (* Port setting *)
    ("port", OInt 3000)
]

end
