#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
int main() {
auto shared = 1;
auto other = 2;
process(shared, 1);
process(std::move(other), 0);
process(shared, 8);
    return 0;
}
