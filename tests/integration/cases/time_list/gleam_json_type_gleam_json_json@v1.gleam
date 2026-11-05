import gleam/json

pub fn main() {
  let my_data: json.Json = json.object([
    #("times", json.preprocessed_array([json.string("09:30:00"), json.string("17:45:00"), json.string("23:59:59")])),
  ])
  let _ = my_data
}
