import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("outer", json.preprocessed_array([json.preprocessed_array([json.string("nested first line\n  indented\n\nnested last line\n")])])),
  ])
  let _ = my_data
}
