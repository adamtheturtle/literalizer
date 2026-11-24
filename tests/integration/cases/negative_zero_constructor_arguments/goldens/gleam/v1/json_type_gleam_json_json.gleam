import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.float(-0.0),
    json.float(0.0),
  ])
  let _ = my_data
}
