template <typename... Args> auto f(Args...) { return 0; }
template <typename... Args> auto repr(Args...) { return 0; }
int main() {
auto ref_data = 1;
repr(f(ref_data));
    return 0;
}
