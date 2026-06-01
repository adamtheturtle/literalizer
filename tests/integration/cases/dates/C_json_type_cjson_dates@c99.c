#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateString("2024-01-15");
cJSON_AddItemToObject(_n0, "date", _n1);
cJSON *_n2 = cJSON_CreateString("2024-01-15T12:30:00+00:00");
cJSON_AddItemToObject(_n0, "datetime", _n2);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
