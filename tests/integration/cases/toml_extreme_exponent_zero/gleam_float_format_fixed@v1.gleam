pub type GVal {
  GFloat(Float)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("value", GFloat(0.000000)),
  ])
  let _ = my_data
}
