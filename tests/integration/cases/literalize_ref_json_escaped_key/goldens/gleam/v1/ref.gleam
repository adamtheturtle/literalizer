pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_var = GDict([
    #("_", GStr("_")),
  ])
  let my_data = my_var
  let _ = my_data
}
