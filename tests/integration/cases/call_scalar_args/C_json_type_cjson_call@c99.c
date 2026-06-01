#include <cjson/cJSON.h>
static void process(CVal _a0) { (void)_a0; }
int main(void) {
process(((CVal){.s = "hello"}));
process(((CVal){.i = 42}));
process(((CVal){.b = true}));
    return 0;
}
