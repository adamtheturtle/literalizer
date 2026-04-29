pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_var = GInt(0)
  let my_data = GDict([
    #("key", my_var),
  ])
  let _ = my_data
}
