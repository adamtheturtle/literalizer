module Check = struct

type val_t =
  | OFloat of float
  | OStr of string
  | OList of val_t list
module Throttler = struct
let check _ = ()
end
let emit _ = ()
let _ = emit(Throttler.check("user_1", 1000.0))
let _ = emit(Throttler.check("user_2", 2000.5))

end
