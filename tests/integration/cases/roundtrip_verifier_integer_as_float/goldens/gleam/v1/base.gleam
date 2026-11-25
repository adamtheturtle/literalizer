pub type GVal {
  GFloat(Float)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("value", GFloat(1.0)),
  ])
  let _ = my_data
}
