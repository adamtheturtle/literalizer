with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("id", AInt (100)), AEntry ("description", AStr ("first task")), AEntry ("is_done", ABool (False)), AEntry ("blocks", AList'[AInt (102), AInt (103)])],
        AMap'[AEntry ("id", AInt (101)), AEntry ("description", AStr ("second task")), AEntry ("is_done", ABool (True)), AEntry ("blocks", AList'[])]
    ];
begin
    my_data := AList'[
        AMap'[AEntry ("id", AInt (100)), AEntry ("description", AStr ("first task")), AEntry ("is_done", ABool (False)), AEntry ("blocks", AList'[AInt (102), AInt (103)])],
        AMap'[AEntry ("id", AInt (101)), AEntry ("description", AStr ("second task")), AEntry ("is_done", ABool (True)), AEntry ("blocks", AList'[])]
    ];
end Main;
