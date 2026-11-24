pub type GVal {
  GBool(Bool)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("keep", GBool(True)),
    #("skip", GBool(False)),
  ])
  let _ = my_data
}
