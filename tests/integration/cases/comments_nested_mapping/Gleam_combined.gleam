import gleam/dict

pub fn main() {
  let my_data = dict.from_list([
    #("a", dict.from_list([#("x", 1)])),
    #("b", 2),
  ])
  let my_data = dict.from_list([
    #("a", dict.from_list([#("x", 1)])),
    #("b", 2),
  ])
  let _ = my_data
}
