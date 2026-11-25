import gleam/json

pub fn main() {
  let my_data: json.Json = json.preprocessed_array([
    json.preprocessed_array([json.string("set_task"), json.string("web"), json.string("lint_web")]),
    json.preprocessed_array([json.string("merge_pipelines")]),
  ])
  let _ = my_data
}
