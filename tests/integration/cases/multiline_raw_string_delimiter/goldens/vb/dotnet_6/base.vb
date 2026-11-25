Imports System.Collections.Generic
Module Check
    Dim my_data = New String() {
        "custom base after empty collision: )""" & Chr(10) & "value",
        "custom suffix after base collision: )"" and )x0""" & Chr(10) & "value",
        "custom second suffix: )"" and )x0"" and )x00""" & Chr(10) & "value",
        "long base exhaustion: )"" and )abcdefghijklmnop""" & Chr(10) & "value"
    }
End Module
