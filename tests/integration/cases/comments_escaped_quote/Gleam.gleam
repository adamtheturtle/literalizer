import gleam/dict

pub fn main() {
  let my_data = dict.from_list([
    #("key", "value \" # not a comment"),  // real
  ])
  let _ = my_data
}
