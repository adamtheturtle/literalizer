procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AList'(
            AMap'(AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_1")), AEntry ("draft", ABool (True))),
            AMap'(AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_2")))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AList'(
            AMap'(AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_1")), AEntry ("draft", ABool (True))),
            AMap'(AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_2")))
        );
    end Check_Assignment;
begin
    null;
end Check;
