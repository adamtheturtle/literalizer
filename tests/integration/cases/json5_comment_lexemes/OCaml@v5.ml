module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    (* heading *)
    ("a", OStr "single ' // data");
    ("b", OStr "linecontinuation");
    ("c", OStr "\\");  (* actual comment *)
    ("d", OStr "  ")  (* final comment *)
]

end
