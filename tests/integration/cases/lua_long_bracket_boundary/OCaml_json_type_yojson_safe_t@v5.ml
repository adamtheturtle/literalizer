module Check = struct

let my_data : Yojson.Safe.t = `List [
    `String "]";
    `String "a]";
    `String "a]=";
    `String "a]b"
]

end
