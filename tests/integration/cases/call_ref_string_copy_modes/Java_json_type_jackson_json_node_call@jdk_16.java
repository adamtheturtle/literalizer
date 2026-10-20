import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object consume(Object arg0) { return null; }
    public static void main() throws Exception {
JsonNode item = new ObjectMapper().readTree("\"s\"");
consume(item);
    }
}
