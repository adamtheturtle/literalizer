module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("test", `List [`Int 5; `List [`String "compile"; `String "test"]]);
    ("package", `List [`Int 7; `List [`String "link"; `String "test"]])
]

end
