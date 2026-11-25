import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.object([#("", json.string("external_value"))]),
  ])
  let _ = my_data
}
