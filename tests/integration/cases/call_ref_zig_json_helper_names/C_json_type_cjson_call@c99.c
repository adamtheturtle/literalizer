#include <cjson/cJSON.h>
static void process(cJSON *_a0) { (void)_a0; }
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(_n0, "a", _n1);
cJSON *arena = _n0;
cJSON *_n2 = cJSON_CreateObject();
cJSON *_n3 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(_n2, "a", _n3);
cJSON *ZVal = _n2;
cJSON *_n4 = cJSON_CreateObject();
cJSON *_n5 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(_n4, "a", _n5);
cJSON *ZKV = _n4;
process(arena);
process(ZVal);
process(ZKV);
    return 0;
}
