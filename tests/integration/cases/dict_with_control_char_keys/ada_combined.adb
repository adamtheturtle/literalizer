procedure Check is
   procedure Check_Declaration is
      my_data : A_Val := AMap'(
          AEntry ("key\nwith\nnewlines", AStr ("value1")),
          AEntry ("key	with	tabs", AStr ("value2"))
      );
   begin
      null;
   end Check_Declaration;
   procedure Check_Assignment is
   begin
      my_data := AMap'(
          AEntry ("key\nwith\nnewlines", AStr ("value1")),
          AEntry ("key	with	tabs", AStr ("value2"))
      );
   end Check_Assignment;
begin
   Check_Declaration;
   Check_Assignment;
end Check;
