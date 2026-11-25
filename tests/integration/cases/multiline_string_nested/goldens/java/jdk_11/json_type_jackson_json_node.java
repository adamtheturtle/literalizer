import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("{\"outer\": [[\"nested first line\\n  indented\\n\\nnested last line\\n\"]]}");
    }
}
