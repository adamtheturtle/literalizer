import gleam/dict

pub fn main() {
  let my_data = dict.from_list([
    // Server configuration
    #("host", "localhost"),  // default host
    #("port", 8080),
    // Enable debug mode
    #("debug", True),
  ])
  let _ = my_data
}
