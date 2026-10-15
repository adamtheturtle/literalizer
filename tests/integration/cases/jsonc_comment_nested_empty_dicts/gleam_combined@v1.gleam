pub type GVal {
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    // outer heading
    // first empty
    #("a", GDict([])),
    // second empty
    #("b", GDict([])),
  ])
  let _ = my_data
  let my_data = GDict([
    // outer heading
    // first empty
    #("a", GDict([])),
    // second empty
    #("b", GDict([])),
  ])
  let _ = my_data
}
