IDENTIFICATION DIVISION.
PROGRAM-ID. CHECK.
DATA DIVISION.
WORKING-STORAGE SECTION.
01 MY-DATA.
    05 F-USERS.

        10 FILLER.

            15 F-NAME PIC X(3) VALUE "Bob".
            15 F-TAGS.

                20 FILLER PIC X(5) VALUE "admin".
                20 FILLER PIC X(4) VALUE "user".


        10 FILLER.

            15 F-NAME PIC X(5) VALUE "Carol".
            15 F-TAGS.

                20 FILLER PIC X(5) VALUE "guest".
PROCEDURE DIVISION.
    STOP RUN.
