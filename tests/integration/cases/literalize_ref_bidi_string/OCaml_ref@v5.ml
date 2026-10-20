module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let text : val_t = OStr "a‪b"
let my_data : val_t = OMap [
    ("value", text)
]

end
