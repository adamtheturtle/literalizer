object Fixture_call_snake_dotted_method_Scala_heterogeneous_strategy_record_call {
class _Http_clientType { def fetch(payload: Any = null): Any = null }
class _My_appType { val http_client = new _Http_clientType }
val my_app = new _My_appType
my_app.http_client.fetch(payload = "hello")
my_app.http_client.fetch(payload = 42)
my_app.http_client.fetch(payload = true)
}
