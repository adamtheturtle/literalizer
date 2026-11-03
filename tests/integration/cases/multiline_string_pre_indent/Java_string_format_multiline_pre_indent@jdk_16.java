
class Main {
    public static void main() {
    var my_data = """

first line
\s\sindented

last line
""";
        if (!my_data.equals("\nfirst line\n  indented\n\nlast line\n")) { throw new AssertionError(); }
    }
}
