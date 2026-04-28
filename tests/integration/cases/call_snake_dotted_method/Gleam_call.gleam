pub type GVal {
  GBool(Bool)
  GInt(Int)
  GStr(String)
  GList(List(GVal))
}
pub fn my_app_http_client_fetch(_payload: a) -> Nil { panic }

pub fn main() {
  my_app_http_client_fetch(GStr("hello"))
  my_app_http_client_fetch(GInt(42))
  my_app_http_client_fetch(GBool(True))
}
