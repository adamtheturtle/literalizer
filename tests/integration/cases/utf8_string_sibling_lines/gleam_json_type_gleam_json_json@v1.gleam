import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.string("中中中中中中中中中中中中中中中中中中中中"),
    json.string("é'é'é'é'é'é'é'é'é'é'"),
    json.string("🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"),
  ])
  let _ = my_data
}
