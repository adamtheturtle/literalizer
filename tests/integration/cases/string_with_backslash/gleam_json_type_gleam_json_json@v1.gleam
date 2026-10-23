import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("C:\\path\\to\\file"),
    json.string("back\\\\slash"),
    json.string("hello \\\"world\\\""),
    json.string("path\\to \"# file"),
    json.string("trailing\\"),
    json.string("both \"quotes''' here"),
    json.string("line1\\nline2\nwith newline"),
  ])
  let _ = my_data
}
