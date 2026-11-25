import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("2024-01-15"),
    json.string("2024-06-01"),
  ])
  let _ = my_data
}
