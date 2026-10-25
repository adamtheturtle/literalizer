#include <initializer_list>
auto process(auto...) { return 0; }
int main() {
static_cast<void>(process(1));
    return 0;
}
