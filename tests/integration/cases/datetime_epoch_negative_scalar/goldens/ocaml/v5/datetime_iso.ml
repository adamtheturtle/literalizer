module Check = struct

type val_t =
  | OStr of string
let my_data : val_t = OStr "1969-12-31T23:59:59+00:00"

end
