#include <cjson/cJSON.h>
static void obj_ZVal_stub_(cJSON *_a0) { (void)_a0; }
struct objType_ { void (*ZVal)(cJSON *); };
static const struct objType_ obj = { .ZVal = obj_ZVal_stub_ };
int main(void) {
obj.ZVal(cJSON_CreateNumber((double)1));
    return 0;
}
