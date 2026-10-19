pub type GVal {
  GStr(String)
  GList(List(GVal))
}

pub fn main() {
  let my_data = GList([
    GStr("中中中中中中中中中中中中中中中中中中中中"),
    GStr("é'é'é'é'é'é'é'é'é'é'"),
    GStr("🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"),
  ])
  let _ = my_data
  let my_data = GList([
    GStr("中中中中中中中中中中中中中中中中中中中中"),
    GStr("é'é'é'é'é'é'é'é'é'é'"),
    GStr("🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"),
  ])
  let _ = my_data
}
