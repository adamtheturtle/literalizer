module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
module Foo = struct
let class _ = ()
end
let _ = Foo.class(OInt 1)

end
