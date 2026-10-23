module Check = struct

let my_data : Yojson.Safe.t = `List [
    `String "C:\\path\\to\\file";
    `String "back\\\\slash";
    `String "hello \\\"world\\\"";
    `String "path\\to \"# file";
    `String "trailing\\";
    `String "both \"quotes''' here";
    `String "line1\\nline2\nwith newline"
]

end
