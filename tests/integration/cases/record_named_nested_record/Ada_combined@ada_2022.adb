with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("project", AStr ("alpha")),
        AEntry ("lead_task", AMap'[AEntry ("id", AInt (100)), AEntry ("description", AStr ("first task")), AEntry ("is_done", ABool (False)), AEntry ("blocks", AList'[AInt (102), AInt (103)])])
    ];
begin
    my_data := AMap'[
        AEntry ("project", AStr ("alpha")),
        AEntry ("lead_task", AMap'[AEntry ("id", AInt (100)), AEntry ("description", AStr ("first task")), AEntry ("is_done", ABool (False)), AEntry ("blocks", AList'[AInt (102), AInt (103)])])
    ];
end Main;
