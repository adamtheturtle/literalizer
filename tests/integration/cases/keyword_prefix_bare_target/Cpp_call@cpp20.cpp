#include <initializer_list>
auto first_value(auto...) { return 0; }
int main() {
first_value(1);
    return 0;
}
