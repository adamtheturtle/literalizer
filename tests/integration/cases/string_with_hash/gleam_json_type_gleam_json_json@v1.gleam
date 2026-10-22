import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("issue #{42}"),
    json.string("color #red"),
  ])
  let _ = my_data
}
