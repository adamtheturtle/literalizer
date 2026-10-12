import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
class Main {
static class ObjType_ { Object ZVal(Object... args) { return null; } }
static ObjType_ obj = new ObjType_();
    public static void main() throws Exception {
obj.ZVal(new ObjectMapper().readTree("1"));
    }
}
