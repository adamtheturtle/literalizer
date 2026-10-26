import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("SGVsbG8="),
    json.preprocessed_array([]),
  ])
  let _ = my_data
}
