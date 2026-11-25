pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("ts", GStr("3000-12-31T23:59:59.999999+00:00")),
  ])
  let _ = my_data
}
