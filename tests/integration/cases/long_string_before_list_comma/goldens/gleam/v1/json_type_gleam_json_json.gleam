import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("This long string keeps its structural comma beyond the Fortran wrapping window without a safe split."),
    json.int(1),
  ])
  let _ = my_data
}
