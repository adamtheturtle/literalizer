object Check {
import scala.language.dynamics
object throttler extends Dynamic { def applyDynamicNamed(n: String)(a: (String, Any)*): Any = null }
import scala.language.dynamics
object print extends Dynamic { def applyDynamic(n: String)(a: Any*): Any = null }
print(throttler.check(user_id = "user_1", ts = 1000.0))
print(throttler.check(user_id = "user_2", ts = 2000.5))
}
