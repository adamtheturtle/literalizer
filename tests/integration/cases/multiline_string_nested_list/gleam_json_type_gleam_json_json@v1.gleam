import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.preprocessed_array([json.string("\nfirst line\n  indented\n\nlast line\n")]),
  ])
  let _ = my_data
}
