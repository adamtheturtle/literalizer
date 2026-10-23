module Check = struct

let my_data : Yojson.Safe.t = `List [
    `String "café";
    `String "中文";
    `String "😀"
]

end
