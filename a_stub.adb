package body A_Stub is

   function Empty return A_Val is
   begin
      return (null record);
   end Empty;

   procedure Append (Container : in out A_Val; Item : A_Val) is
   begin
      null;
   end Append;

   function AStr (S : String) return A_Val is
   begin
      return (null record);
   end AStr;

   function AStr (C : Character) return A_Val is
   begin
      return (null record);
   end AStr;

   function AInt (I : Long_Long_Integer) return A_Val is
   begin
      return (null record);
   end AInt;

   function AFloat (F : Long_Float) return A_Val is
   begin
      return (null record);
   end AFloat;

   function ABool (B : Boolean) return A_Val is
   begin
      return (null record);
   end ABool;

   function AEntry (Key : String; Value : A_Val) return A_Val is
   begin
      return (null record);
   end AEntry;

   function A_Pos_Inf return A_Val is
   begin
      return (null record);
   end A_Pos_Inf;

   function A_Neg_Inf return A_Val is
   begin
      return (null record);
   end A_Neg_Inf;

   function A_NaN return A_Val is
   begin
      return (null record);
   end A_NaN;

end A_Stub;
