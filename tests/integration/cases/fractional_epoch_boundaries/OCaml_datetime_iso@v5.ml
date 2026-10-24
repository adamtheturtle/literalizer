module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OStr "1970-01-01T00:00:00.000001+00:00";
    OStr "1969-12-31T23:59:59.500000+00:00";
    OStr "1970-01-01T00:00:01+00:00"
]

end
