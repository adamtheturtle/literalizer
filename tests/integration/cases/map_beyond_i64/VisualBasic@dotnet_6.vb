Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", 9223372036854775807UL},
        {"b", 9223372036854775808UL}
    }
End Module
