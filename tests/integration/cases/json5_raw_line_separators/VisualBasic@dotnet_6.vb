Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"double", "a     b"},
        {"single", "c     d"},
        {"both", "e     f     g"},
        {"continued", "hi"},
        {"escaped backslash", "j\     k"}
    }
End Module
