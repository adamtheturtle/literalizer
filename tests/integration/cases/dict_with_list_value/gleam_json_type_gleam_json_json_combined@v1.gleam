import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("name", json.string("Alice")),
    #("scores", json.preprocessed_array([json.int(10), json.int(20), json.int(30)])),
  ])
  let my_data: json.Json = json.object([
    #("name", json.string("Alice")),
    #("scores", json.preprocessed_array([json.int(10), json.int(20), json.int(30)])),
  ])
  let _ = my_data
}
