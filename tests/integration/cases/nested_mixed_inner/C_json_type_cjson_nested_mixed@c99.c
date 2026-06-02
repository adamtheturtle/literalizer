#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateArray();
cJSON *_n1 = cJSON_CreateArray();
cJSON *_n2 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(_n1, _n2);
cJSON *_n3 = cJSON_CreateString("a");
cJSON_AddItemToArray(_n1, _n3);
cJSON_AddItemToArray(_n0, _n1);
cJSON *_n4 = cJSON_CreateArray();
cJSON *_n5 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(_n4, _n5);
cJSON *_n6 = cJSON_CreateString("b");
cJSON_AddItemToArray(_n4, _n6);
cJSON_AddItemToArray(_n0, _n4);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
