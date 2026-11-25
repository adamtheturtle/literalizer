import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("test", json.preprocessed_array([json.int(5), json.preprocessed_array([json.string("compile"), json.string("test")])])),
    #("package", json.preprocessed_array([json.int(7), json.preprocessed_array([json.string("link"), json.string("test")])])),
  ])
  let _ = my_data
}
