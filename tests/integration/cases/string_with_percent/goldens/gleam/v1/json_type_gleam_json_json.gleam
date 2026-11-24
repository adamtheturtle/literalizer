import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("100% done"),
    json.string("%(name) is here"),
  ])
  let _ = my_data
}
