pub type GVal {
  GDict(List(#(String, GVal)))
}

pub fn main() {
  // empty heading
  // empty body
  // after empty
  let my_data = GDict([])
  let _ = my_data
  // empty heading
  // empty body
  // after empty
  let my_data = GDict([])
  let _ = my_data
}
