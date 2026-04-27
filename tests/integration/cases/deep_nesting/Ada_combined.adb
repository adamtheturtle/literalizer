procedure Check is
    procedure Check_Declaration is
        my_data : A_Val := AMap'(
            AEntry ("level1", AMap'(AEntry ("level2", AMap'(AEntry ("level3", AMap'(AEntry ("level4", AMap'(AEntry ("value", AStr ("deep")), AEntry ("items", AList'(AStr ("a"), AStr ("b"))))))), AEntry ("sibling", AInt (42)))), AEntry ("tags", AList'(AMap'(AEntry ("name", AStr ("tag1")), AEntry ("meta", AMap'(AEntry ("priority", AInt (1)), AEntry ("labels", AList'(AStr ("x"), AStr ("y"))))))))))
        );
    begin
        null;
    end Check_Declaration;
    procedure Check_Assignment is
    begin
        my_data := AMap'(
            AEntry ("level1", AMap'(AEntry ("level2", AMap'(AEntry ("level3", AMap'(AEntry ("level4", AMap'(AEntry ("value", AStr ("deep")), AEntry ("items", AList'(AStr ("a"), AStr ("b"))))))), AEntry ("sibling", AInt (42)))), AEntry ("tags", AList'(AMap'(AEntry ("name", AStr ("tag1")), AEntry ("meta", AMap'(AEntry ("priority", AInt (1)), AEntry ("labels", AList'(AStr ("x"), AStr ("y"))))))))))
        );
    end Check_Assignment;
begin
    null;
end Check;
