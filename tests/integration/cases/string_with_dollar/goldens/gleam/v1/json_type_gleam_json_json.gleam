import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("price $10"),
    json.string("$HOME"),
  ])
  let _ = my_data
}
