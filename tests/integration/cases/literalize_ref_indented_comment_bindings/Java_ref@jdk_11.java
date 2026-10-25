class Main {
    public static void main() {
        var shared = new int[]{
            1,
            2
        };
        var my_data = new Object[]{
            // A leading comment with { braces, "quotes", and // markers
            "first\n{ \"quoted\" // text }",
            shared
        };
    }
}
