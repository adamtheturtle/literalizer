module Check = struct

type val_t =
  | OFloat of float
  | OStr of string
  | OList of val_t list
module Throttler = struct
let check _ _ = ()
end
let _ = Throttler.check ("user_1") (1000.0)
let _ = Throttler.check ("user_2") (2000.5)

end
