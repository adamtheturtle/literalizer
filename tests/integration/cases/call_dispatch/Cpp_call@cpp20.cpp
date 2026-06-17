#include <initializer_list>
#include <vector>
auto put(auto...) { return 0; }
auto get(auto...) { return 0; }
int main() {
put(1, 10);
get(1);
    return 0;
}
