#include <initializer_list>
#include <vector>
auto store_item(auto...) { return 0; }
auto read_item(auto...) { return 0; }
int main() {
store_item(1, 10);
read_item(1);
    return 0;
}
