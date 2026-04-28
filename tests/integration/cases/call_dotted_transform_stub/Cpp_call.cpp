#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
struct logType_ { auto emit(auto...) const { return 0; } };
const logType_ log;
int main() {
log.emit(process("hello"));
log.emit(process(42));
log.emit(process(true));
    return 0;
}
