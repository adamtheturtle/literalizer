#include <initializer_list>
#include <string>
#include <vector>
auto op(auto...) { return 0; }
int main() {
op("hello");
    return 0;
}
