import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.preprocessed_array([json.preprocessed_array([]), json.preprocessed_array([])]),
    json.preprocessed_array([json.preprocessed_array([json.int(1)]), json.preprocessed_array([json.int(1)])]),
  ])
  let _ = my_data
}
