import gleam/dict
pub fn main() {
  let my_data = [
    #("name", "Alice"),
    #("scores", dict.from_list([#("1", "first"), #("2", "second")])),
  ]
  let _ = my_data
}
