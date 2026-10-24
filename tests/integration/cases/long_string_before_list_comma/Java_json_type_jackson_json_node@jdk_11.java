import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
    public static void main() throws Exception {
JsonNode my_data = new ObjectMapper().readTree("[\"This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.\", 1]");
    }
}
