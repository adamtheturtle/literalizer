import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("48656c6c6f"),
  ])
  let _ = my_data
}
