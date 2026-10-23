module Check = struct

type val_t =
  | OStr of string
  | OArray of val_t array
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("times", OArray [|OStr "09:30:00"; OStr "17:45:00"; OStr "23:59:59"|])
]

end
