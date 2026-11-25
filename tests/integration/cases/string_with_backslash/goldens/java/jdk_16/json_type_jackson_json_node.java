import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("[\"C:\\\\path\\\\to\\\\file\", \"back\\\\\\\\slash\", \"hello \\\\\\\"world\\\\\\\"\", \"path\\\\to \\\"# file\", \"trailing\\\\\", \"both \\\"quotes''' here\", \"line1\\\\nline2\\nwith newline\"]");
    }
}
