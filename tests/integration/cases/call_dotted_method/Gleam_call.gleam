pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn app_client_fetch(_payload: a) -> Nil { panic }

pub fn main() {
  app_client_fetch(GStr("hello"))
  app_client_fetch(GInt(42))
  app_client_fetch(GBool(True))
}
