import gleam/dict

pub fn main() {
  let my_data = dict.from_list([
    #("name", "Alice"),
    #("score", Nil),
    #("age", 30),
  ])
  let _ = my_data
}
