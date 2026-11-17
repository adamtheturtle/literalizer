final my_data = null;
void main() {
    var my_data = "seed";
    my_data = "${"// payload"};"; if (my_data != "// payload;") throw StateError("incorrect interpolation");
}
