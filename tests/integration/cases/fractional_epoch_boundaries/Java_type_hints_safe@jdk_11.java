import java.time.Instant;
class Main {
    public static void main() {
var my_data = new Object[]{
    Instant.parse("1970-01-01T00:00:00.000001+00:00"),
    Instant.parse("1969-12-31T23:59:59.500000+00:00"),
    Instant.parse("1970-01-01T00:00:01+00:00")
};
    }
}
