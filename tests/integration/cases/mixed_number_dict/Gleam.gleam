import gleam/dict

pub fn main() {
  let my_data = dict.from_list([
    #("a", 1),
    #("b", 2.5),
    #("c", 3),
  ])
  let _ = my_data
}
