pub type GVal {
  GStr(String)
  GList(List(GVal))
}
pub fn app_client_fetch(_value: a) -> Nil { Nil }

pub fn main() {
  app_client_fetch(GStr("hello"))
  app_client_fetch(GStr("world"))
}
