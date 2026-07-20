#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
int main() {
auto my_data = process(1, 2);
    (void)my_data;
    return 0;
}
