Imports System.Collections.Generic
Module Check
    Dim my_data = New String() {
        "C:\path\to\file",
        "back\\slash",
        "hello \""world\""",
        "path\to ""# file",
        "trailing\",
        "both ""quotes''' here",
        "line1\nline2" & Chr(10) & "with newline"
    }
End Module
