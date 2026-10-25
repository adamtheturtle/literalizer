#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateString("value");
cJSON_AddItemToObject(literalizer_my_data_n0, "08", literalizer_my_data_n1);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
