import gleam/dict
pub fn main() {
  let my_data = dict.from_list([
    // Configuration
    #("name", "app"),
    // Port setting
    #("port", 3000),
  ])
  let _ = my_data
}
