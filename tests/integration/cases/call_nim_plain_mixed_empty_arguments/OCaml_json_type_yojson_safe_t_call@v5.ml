module Check = struct

let make_widget _ = ()
let _ = make_widget(`List [], `List [`Int 1], `List [])
let _ = make_widget(`List [`String "text"], `List [`Int 2], `List [])
let _ = make_widget(`List [], `List [`String "text"], `List [])
let _ = make_widget(`List [`String "text"], `List [`Int 2], `List [`Int 3])

end
