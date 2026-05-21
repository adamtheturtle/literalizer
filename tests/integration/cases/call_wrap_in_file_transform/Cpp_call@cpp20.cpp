#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
int main() {
process(1, 2);
    return 0;
}
