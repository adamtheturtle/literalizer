import java.lang.reflect.Array;
import java.math.BigInteger;
import java.util.Map;

// Serialize a value back to JSON for the Java round-trip check driven by
// `.github/scripts/run_java_roundtrip.py` (invoked from the `Java
// roundtrip` step of the `lint-fast` job in
// `.github/workflows/lint.yml`, which is where the JDK toolchain is set
// up). The runner literalizes the shared `roundtrip_input.json`
// document to a Java `var myData = ...;` declaration, generates a tiny
// `Main` that calls
// `JavaRoundtripSerializer.toJson(myData)`, and compiles this file
// alongside it (the same standalone-`.java`-helper pattern as
// `CheckJavaSyntax.java`, kept out of the pytest suite and out of a
// Python string so it stays real, highlightable, compilable Java).
//
// `toJson` covers exactly the types the default `Java()` config in
// `src/literalizer/languages/java.py` emits for null-free JSON:
// `java.util.Map` (from `Map.ofEntries`), primitive/Object arrays (via
// `java.lang.reflect.Array`, so `int[]`/`double[]`/`boolean[]`/`Object[]`
// share one path because `Array.get` auto-boxes), `String`, `Boolean`,
// `Integer`, `Long`, `BigInteger` and `Double`. `Double.toString` emits
// the shortest round-tripping form, which Python `json.loads` reparses to
// the equal float. `Map.ofEntries` iteration order is unspecified, but
// Python `dict` equality is order-independent; arrays preserve order.
// JSON `null` is intentionally unsupported (see the runner docstring).
final class JavaRoundtripSerializer {
    private JavaRoundtripSerializer() {
    }

    static String toJson(final Object o) {
        if (o == null) {
            return "null";
        }
        if (o instanceof Boolean || o instanceof Integer
                || o instanceof Long || o instanceof BigInteger) {
            return o.toString();
        }
        if (o instanceof Double) {
            return Double.toString((Double) o);
        }
        if (o instanceof String) {
            final String s = (String) o;
            final StringBuilder b = new StringBuilder();
            b.append('"');
            for (int i = 0; i < s.length(); i++) {
                final char c = s.charAt(i);
                if (c == '\\' || c == '"') {
                    b.append('\\');
                    b.append(c);
                } else if (c < 0x20) {
                    b.append(String.format("\\u%04x", (int) c));
                } else {
                    b.append(c);
                }
            }
            b.append('"');
            return b.toString();
        }
        if (o instanceof Map) {
            final StringBuilder b = new StringBuilder("{");
            boolean first = true;
            for (final Map.Entry<?, ?> e : ((Map<?, ?>) o).entrySet()) {
                if (!first) {
                    b.append(",");
                }
                first = false;
                b.append(toJson(e.getKey().toString()));
                b.append(":");
                b.append(toJson(e.getValue()));
            }
            b.append("}");
            return b.toString();
        }
        if (o.getClass().isArray()) {
            final StringBuilder b = new StringBuilder("[");
            final int n = Array.getLength(o);
            for (int i = 0; i < n; i++) {
                if (i > 0) {
                    b.append(",");
                }
                b.append(toJson(Array.get(o, i)));
            }
            b.append("]");
            return b.toString();
        }
        throw new IllegalArgumentException("unhandled " + o.getClass());
    }
}
