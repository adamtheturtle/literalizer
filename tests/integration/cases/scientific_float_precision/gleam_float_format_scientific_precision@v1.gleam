pub type GVal {
  GFloat(Float)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("pi", GFloat(3.141592653589793)),
  ])
  let _ = my_data
}
