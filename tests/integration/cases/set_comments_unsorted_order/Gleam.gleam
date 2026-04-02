import gleam/set

pub fn main() {
  let my_data = set.from_list([
    // before apple
    "apple",
    "banana",  // banana inline
    // trailing
  ])
  let _ = my_data
}
