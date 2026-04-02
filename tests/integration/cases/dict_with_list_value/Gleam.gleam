import gleam/dict
pub fn main() {
  let my_data = dict.from_list([
    #("name", "Alice"),
    #("scores", [10, 20, 30]),
  ])
  let _ = my_data
}
