module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("cr", OStr "a\rb");
    ("crlf", OStr "a\r\nb");
    ("lf", OStr "a\nb")
]

end
