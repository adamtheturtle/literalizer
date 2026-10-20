#include <initializer_list>
auto process(auto...) { return 0; }
int main() {
auto my_data = process(1);
    (void)my_data;
    return 0;
}
