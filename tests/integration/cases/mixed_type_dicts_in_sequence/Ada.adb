procedure Check is
    my_data : A_Val := AList'(
        AMap'(AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_1")), AEntry ("draft", ABool (True))),
        AMap'(AEntry ("type", AStr ("create")), AEntry ("pr_id", AStr ("pr_2")))
    );
begin
    null;
end Check;
