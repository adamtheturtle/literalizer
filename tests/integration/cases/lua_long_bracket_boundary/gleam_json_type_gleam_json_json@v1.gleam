import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("]"),
    json.string("a]"),
    json.string("a]="),
    json.string("a]b"),
  ])
  let _ = my_data
}
