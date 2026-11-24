import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("[[\"\\nfirst line\\n  indented\\n\\nlast line\\n\"]]");
    }
}
