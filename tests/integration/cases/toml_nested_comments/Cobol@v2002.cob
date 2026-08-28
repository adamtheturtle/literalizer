IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 MY-DATA.
    *> About the first dotted key.
    *> About the second dotted key.
    05 F-DOTTED.
    10 F-FIRST PIC S9(18) COMP-5 VALUE 1.  *> About the plain key.
    *> Inside the table.
    10 F-SECOND PIC S9(18) COMP-5 VALUE 2.
    *> Before the first entry.
    *> Before the second entry.
    05 F-PLAIN PIC S9(18) COMP-5 VALUE 3.
    05 F-TABLE.
    10 F-INNER PIC S9(18) COMP-5 VALUE 4.
    05 F-ENTRIES.
    10 F-NAME PIC X(3) VALUE "one".
    10 F-NAME-2 PIC X(3) VALUE "two".
PROCEDURE DIVISION.
    STOP RUN.
