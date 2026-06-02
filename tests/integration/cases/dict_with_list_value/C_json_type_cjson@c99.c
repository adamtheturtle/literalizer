#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateString("Alice");
cJSON_AddItemToObject(_n0, "name", _n1);
cJSON *_n2 = cJSON_CreateArray();
cJSON *_n3 = cJSON_CreateNumber((double)10);
cJSON_AddItemToArray(_n2, _n3);
cJSON *_n4 = cJSON_CreateNumber((double)20);
cJSON_AddItemToArray(_n2, _n4);
cJSON *_n5 = cJSON_CreateNumber((double)30);
cJSON_AddItemToArray(_n2, _n5);
cJSON_AddItemToObject(_n0, "scores", _n2);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
