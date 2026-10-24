module Check = struct

type val_t =
  | OStr of string
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("half", OStr "1979-05-27T07:32:00.500000");
    ("milli", OStr "1979-05-27T07:32:00.100000");
    ("max_milli", OStr "1979-05-27T07:32:00.999000");
    ("whole", OStr "1979-05-27T07:32:00")
]

end
