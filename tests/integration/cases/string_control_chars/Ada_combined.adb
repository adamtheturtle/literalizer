procedure Check is
   procedure Check_Declaration is
      my_data : A_Val := AList'(
          AStr ("line1\nline2"),
          AStr ("line1line2"),
          AStr ("")
      );
   begin
      null;
   end Check_Declaration;
   procedure Check_Assignment is
   begin
      my_data := AList'(
          AStr ("line1\nline2"),
          AStr ("line1line2"),
          AStr ("")
      );
   end Check_Assignment;
begin
   Check_Declaration;
   Check_Assignment;
end Check;
