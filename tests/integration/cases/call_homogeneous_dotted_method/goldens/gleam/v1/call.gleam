pub type GVal {
  GStr(String)
  GList(List(GVal))
}
pub fn app_client_fetch(_value: a) -> Nil { Nil }

pub fn main() {
  let _ = app_client_fetch(GStr("hello"))
  let _ = app_client_fetch(GStr("world"))
}
