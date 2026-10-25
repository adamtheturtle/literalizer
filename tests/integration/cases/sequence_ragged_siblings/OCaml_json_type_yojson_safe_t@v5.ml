module Check = struct

let my_data : Yojson.Safe.t = `List [
    `List [`String "set_task"; `String "web"; `String "lint_web"];
    `List [`String "merge_pipelines"]
]

end
