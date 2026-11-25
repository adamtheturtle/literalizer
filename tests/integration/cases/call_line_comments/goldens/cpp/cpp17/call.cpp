template <typename... Args> auto process(Args...) { return 0; }
int main() {
process("Dune");  // first edition
process("Solaris");
process("Neuromancer");  // cyberpunk
    return 0;
}
