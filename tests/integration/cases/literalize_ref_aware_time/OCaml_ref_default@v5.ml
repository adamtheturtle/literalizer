module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let shared_time : val_t = OStr "12:30:15+02:00"
let my_data : val_t = OMap [
    ("x", shared_time)
]

end
