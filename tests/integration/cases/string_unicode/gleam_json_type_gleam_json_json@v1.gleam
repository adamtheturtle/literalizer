import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("café"),
    json.string("中文"),
    json.string("😀"),
  ])
  let _ = my_data
}
