#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateArray();
cJSON *_n1 = cJSON_CreateNumber((double)-42);
cJSON_AddItemToArray(_n0, _n1);
cJSON *_n2 = cJSON_CreateNumber((double)0);
cJSON_AddItemToArray(_n0, _n2);
cJSON *_n3 = cJSON_CreateNumber((double)42);
cJSON_AddItemToArray(_n0, _n3);
cJSON *_n4 = cJSON_CreateNumber(-1.25);
cJSON_AddItemToArray(_n0, _n4);
cJSON *_n5 = cJSON_CreateNumber(0.0);
cJSON_AddItemToArray(_n0, _n5);
cJSON *_n6 = cJSON_CreateNumber(1.25);
cJSON_AddItemToArray(_n0, _n6);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
