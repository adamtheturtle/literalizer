import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.bool(True),
    json.bool(False),
    json.bool(True),
  ])
  let _ = my_data
}
