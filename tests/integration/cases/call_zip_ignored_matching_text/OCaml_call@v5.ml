module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
let process _ = ()
let _ = process(OStr "time.Date(2024, time.January, 15, 12, 0, 0, 0, time.UTC)")

end
