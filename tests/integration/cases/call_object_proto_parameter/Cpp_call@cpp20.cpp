#include <initializer_list>
#include <vector>
auto capture(auto...) { return 0; }
int main() {
capture(1);
    return 0;
}
