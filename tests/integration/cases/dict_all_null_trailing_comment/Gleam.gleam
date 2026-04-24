pub type GVal {
  GNull
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("a", GNull),
    #("b", GNull),
    // trailing
  ])
  let _ = my_data
}
