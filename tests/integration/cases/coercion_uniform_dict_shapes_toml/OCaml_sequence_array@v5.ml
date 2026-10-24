module Check = struct

type val_t =
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("_", OArray [|OMap [("type", OStr "create"); ("name", OStr "a")]; OMap [("type", OStr "update"); ("name", OStr "b")]|])
]

end
