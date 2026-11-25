import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.object([#("values", json.preprocessed_array([]))]),
    json.object([]),
  ])
  let _ = my_data
}
