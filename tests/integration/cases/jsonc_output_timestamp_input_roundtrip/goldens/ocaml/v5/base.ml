module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    (* event time *)
    ("when", OStr "2024-01-15T12:34:56+00:00")
]

end
