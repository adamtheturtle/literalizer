#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateArray();
cJSON *_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(_n0, _n1);
cJSON *_n2 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(_n0, _n2);
cJSON *ref_data = _n0;
cJSON * my_data = ref_data;
    (void)my_data;
    return 0;
}
