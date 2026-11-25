pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let a_b_c = GDict([
    #("_", GStr("_")),
  ])
  let my_data = a_b_c
  let _ = my_data
}
