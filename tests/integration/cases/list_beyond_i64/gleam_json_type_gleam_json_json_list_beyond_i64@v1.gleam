import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.int(9223372036854775807),
    json.int(9223372036854775808),
  ])
  let _ = my_data
}
