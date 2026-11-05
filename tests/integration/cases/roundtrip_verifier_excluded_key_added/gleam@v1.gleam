pub type GVal {
  GBool(Bool)
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("keep", GBool(True)),
    #("skip", GInt(0)),
  ])
  let _ = my_data
}
