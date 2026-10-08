#include <initializer_list>
#include <vector>
auto consume(auto...) { return 0; }
int main() {
auto external_value = 1;
consume(external_value);
    return 0;
}
