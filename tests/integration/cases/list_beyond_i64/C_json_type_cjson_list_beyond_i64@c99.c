#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateArray();
cJSON *_n1 = cJSON_CreateNumber((double)9223372036854775807);
cJSON_AddItemToArray(_n0, _n1);
cJSON *_n2 = cJSON_CreateNumber((double)9223372036854775808ULL);
cJSON_AddItemToArray(_n0, _n2);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
