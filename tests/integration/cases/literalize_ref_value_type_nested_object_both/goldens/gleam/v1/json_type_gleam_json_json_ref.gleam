import gleam/json

pub fn main() {
  let shared: json.Json = json.preprocessed_array([
    json.int(1),
    json.int(2),
  ])
  let my_data: json.Json = json.object([
    #("field", shared),
  ])
  let _ = my_data
  let my_data: json.Json = json.object([
    #("field", shared),
  ])
  let _ = my_data
}
