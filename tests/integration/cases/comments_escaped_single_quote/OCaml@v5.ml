module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("key", OStr "it's here")  (* a comment *)
]

end
