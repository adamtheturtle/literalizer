module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("exact_millisecond", OStr "09:30:15.123000");
    ("sub_millisecond", OStr "09:30:15.123456")
]

end
