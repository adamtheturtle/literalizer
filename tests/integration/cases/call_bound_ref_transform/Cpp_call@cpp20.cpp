#include <initializer_list>
#include <vector>
auto f(auto...) { return 0; }
int main() {
auto ref_data = 1;
f(ref_data);
    return 0;
}
