module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_time : val_t = OStr "01:02:03"
let my_data : val_t = OMap [
    ("x", my_time)
]

end
