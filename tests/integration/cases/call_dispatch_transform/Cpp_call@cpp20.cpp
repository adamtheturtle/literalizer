#include <initializer_list>
#include <vector>
auto record_value(auto...) { return 0; }
auto flush_buffer(auto...) { return 0; }
auto emit(auto...) { return 0; }
int main() {
emit(record_value(42));
flush_buffer(3);
    return 0;
}
