import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement
class _ObjType { fun std(value: Any? = null): Any? = null }
val obj = _ObjType()
obj.std(value = Json.parseToJsonElement("1"))
