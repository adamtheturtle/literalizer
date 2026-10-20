module Check = struct

module Thing = struct
let go _ = ()
end
let _ = Thing.go(`List [], `List [`Int 1], `List [])
let _ = Thing.go(`List [`String "text"], `List [`Int 2], `List [])
let _ = Thing.go(`List [], `List [`String "text"], `List [])
let _ = Thing.go(`List [`String "text"], `List [`Int 2], `List [`Int 3])

end
