#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateArray();
cJSON *_n1 = cJSON_CreateBool(1);
cJSON_AddItemToArray(_n0, _n1);
cJSON *_n2 = cJSON_CreateBool(0);
cJSON_AddItemToArray(_n0, _n2);
cJSON *_n3 = cJSON_CreateBool(1);
cJSON_AddItemToArray(_n0, _n3);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
