import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.float(5.0e-324),
    json.float(-5.0e-324),
    json.float(1.0e-310),
  ])
  let _ = my_data
}
