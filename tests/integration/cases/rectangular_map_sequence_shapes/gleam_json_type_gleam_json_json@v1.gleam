import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("a", json.preprocessed_array([json.object([#("item", json.preprocessed_array([json.int(1)]))])])),
    #("b", json.preprocessed_array([json.object([#("item", json.preprocessed_array([json.int(2)]))])])),
  ])
  let _ = my_data
}
