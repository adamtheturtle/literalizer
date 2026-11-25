IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 MY-DATA.
    *>
    *> document heading
    *> before the first entry
    *> after the key
    *> before the value
    05 F-COUNTS.

            *> before the first item
            10 FILLER PIC S9(18) COMP-5 VALUE 1.  *> inline block after the comma
            *> before the second item
            10 FILLER PIC S9(18) COMP-5 VALUE 2.
            *> trailing inside the array
  *> after the nested collection
    05 F-MORE.

            10 FILLER PIC S9(18) COMP-5 VALUE 3.
            *>
            *> block heading
            *> block continuation
            10 FILLER PIC S9(18) COMP-5 VALUE 4.  *> final inline

    *> trailing inside the object
    *> after the root
    *> after the document
PROCEDURE DIVISION.
    INITIALIZE MY-DATA.
    STOP RUN.
