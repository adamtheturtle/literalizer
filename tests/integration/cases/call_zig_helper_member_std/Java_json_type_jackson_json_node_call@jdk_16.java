import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static class ObjType_ { Object std(Object arg0) { return null; } }
static ObjType_ obj = new ObjType_();
    public static void main() throws Exception {
obj.std(new ObjectMapper().readTree("1"));
    }
}
