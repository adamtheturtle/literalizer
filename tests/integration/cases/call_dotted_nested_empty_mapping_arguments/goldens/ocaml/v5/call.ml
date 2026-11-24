module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
module Api = struct
module Worker = struct
let process _ = ()
end
end
let _ = Api.Worker.process(OList [OInt 1; OMap []], OInt 42)
let _ = Api.Worker.process(OList [OInt 2; OMap [("x", OStr "s")]], OInt 43)

end
