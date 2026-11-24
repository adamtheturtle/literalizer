import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object process(Object arg0) { return null; }
static Object emit(Object arg0, Object arg1) { return null; }
    public static void main() throws Exception {
emit(process(new ObjectMapper().readTree("1")), new ObjectMapper().readTree("\"2024-01-15T12:00:00Z\""));
    }
}
