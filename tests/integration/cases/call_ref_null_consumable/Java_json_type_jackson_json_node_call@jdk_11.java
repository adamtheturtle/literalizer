import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static Object consume(Object... args) { return null; }
    public static void main() throws Exception {
JsonNode my_null = new ObjectMapper().readTree("null");
JsonNode regular_null = new ObjectMapper().readTree("null");
consume(my_null);
consume(regular_null);
    }
}
