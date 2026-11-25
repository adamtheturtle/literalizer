import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.int(-42),
    json.int(0),
    json.int(42),
    json.float(-1.25),
    json.float(0.0),
    json.float(1.25),
  ])
  let _ = my_data
}
