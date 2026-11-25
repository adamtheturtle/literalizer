IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
*> scalar heading
*> second heading line
*> scalar inline
*> inline continuation
*> scalar trailing
01 MY-DATA PIC S9(18) COMP-5 VALUE 42.
PROCEDURE DIVISION.
    *> scalar heading
*> second heading line
*> scalar inline
*> inline continuation
*> scalar trailing
MOVE 42 TO MY-DATA.
    STOP RUN.
