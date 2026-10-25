import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("1901-12-13T20:45:51"),
    json.string("1901-12-13T20:45:52"),
    json.string("2038-01-19T03:14:07"),
    json.string("2038-01-19T03:14:08"),
  ])
  let _ = my_data
}
