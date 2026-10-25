pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let user_obj = GDict([
    #("_", GStr("_")),
  ])
  let my_data = user_obj
  let _ = my_data
}
