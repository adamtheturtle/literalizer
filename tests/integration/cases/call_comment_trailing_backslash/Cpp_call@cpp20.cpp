#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
int main() {
process(1);  // trail \ .
process(2);  // second
    return 0;
}
