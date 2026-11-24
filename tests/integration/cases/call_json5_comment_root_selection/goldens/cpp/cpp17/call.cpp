template <typename... Args> auto f(Args...) { return 0; }
int main() {
// selected heading
f(1, 2);  // selected inline
    return 0;
}
