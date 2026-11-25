import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.preprocessed_array([json.int(1), json.string("a")]),
    json.preprocessed_array([json.int(2), json.string("b")]),
  ])
  let _ = my_data
}
