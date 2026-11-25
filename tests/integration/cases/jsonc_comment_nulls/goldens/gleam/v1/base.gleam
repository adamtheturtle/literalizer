pub type GVal {
  GNull
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    // null heading
    // before null
    #("a", GNull),  // first null
    #("b", GNull),  // second null
  ])
  let _ = my_data
}
