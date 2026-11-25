module Check = struct

let my_data : Yojson.Safe.t = `List [
    `String "issue #{42}";
    `String "color #red"
]

end
