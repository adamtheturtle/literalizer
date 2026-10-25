import gleam/json

pub fn main() {
  let shared: json.Json = json.preprocessed_array([
    json.int(1),
    json.int(2),
  ])
  let my_data: json.Json = json.preprocessed_array([
    shared,
    json.int(42),
  ])
  let _ = my_data
}
