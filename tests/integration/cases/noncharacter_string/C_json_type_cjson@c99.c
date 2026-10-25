#include <cjson/cJSON.h>
int main(void) {
cJSON *literalizer_my_data_n0 = cJSON_CreateObject();
cJSON *literalizer_my_data_n1 = cJSON_CreateString("￾");
cJSON_AddItemToObject(literalizer_my_data_n0, "fffe", literalizer_my_data_n1);
cJSON *literalizer_my_data_n2 = cJSON_CreateString("￿");
cJSON_AddItemToObject(literalizer_my_data_n0, "ffff", literalizer_my_data_n2);
cJSON *my_data = literalizer_my_data_n0;
    (void)my_data;
    return 0;
}
