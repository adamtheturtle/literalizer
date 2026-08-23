#include <initializer_list>
#include <string>
#include <vector>
auto self(auto...) { return 0; }
int main() {
self("hello");
    return 0;
}
