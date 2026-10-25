#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateString("2024-01-15T12:00:00Z");
cJSON_AddItemToObject(_n0, "within_i32", _n1);
cJSON *_n2 = cJSON_CreateString("2099-06-15T08:30:00Z");
cJSON_AddItemToObject(_n0, "beyond_i32", _n2);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
