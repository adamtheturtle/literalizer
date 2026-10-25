import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("1960-01-01T00:00:00+00:00"),
  ])
  let _ = my_data
}
