#include <initializer_list>
#include <string>
#include <vector>
auto consume(auto...) { return 0; }
int main() {
const auto* item = "s";
consume(item);
    return 0;
}
