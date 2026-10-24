import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("{\"quote\\\"backslash\\\\\": 1, \"line\\nbreak\": 2, \"$(literal)${text}\": 3, \"RStr prefix\": 4}");
    }
}
