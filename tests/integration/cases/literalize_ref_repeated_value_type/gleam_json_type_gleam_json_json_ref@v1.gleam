import gleam/json

pub fn main() {
  let shared: json.Json = json.int(42)
  let my_data: json.Json = json.preprocessed_array([
    shared,
    shared,
  ])
  let _ = my_data
}
