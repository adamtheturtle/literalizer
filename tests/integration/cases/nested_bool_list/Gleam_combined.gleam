pub type GVal {
  GBool(Bool)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GList([GBool(True), GBool(False)]),
    GList([GBool(True), GBool(True)]),
  ])
  let my_data = GList([
    GList([GBool(True), GBool(False)]),
    GList([GBool(True), GBool(True)]),
  ])
  let _ = my_data
}
