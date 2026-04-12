object Check {
import scala.language.dynamics
object process extends Dynamic { def applyDynamic(n: String)(a: Any*): Any = null }
process(value = "hello")
process(value = 42)
process(value = true)
}
