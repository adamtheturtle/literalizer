import gleam/dict

pub fn main() {
  let my_data = dict.from_list([
    #("key\nwith\nnewlines", "value1"),
    #("key\twith\ttabs", "value2"),
    #("", "value3"),
  ])
  let _ = my_data
}
