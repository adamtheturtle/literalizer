#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
template <typename... Args> auto process(Args...) { return 0; }
struct tracerType_ { template <typename... Args> void emit(Args...) const {} };
const tracerType_ tracer;
int main() {
tracer.emit(process("hello"));
tracer.emit(process(42));
tracer.emit(process(true));
    return 0;
}
