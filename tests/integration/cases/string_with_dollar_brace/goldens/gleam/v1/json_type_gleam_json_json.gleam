import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("prefix ${HOME} suffix"),
    json.string("${interpolated}"),
  ])
  let _ = my_data
}
