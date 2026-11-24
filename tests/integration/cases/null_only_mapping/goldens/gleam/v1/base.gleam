pub type GVal {
  GNull
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("value", GNull),
  ])
  let _ = my_data
}
