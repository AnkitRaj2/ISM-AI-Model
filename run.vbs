Set oShell = CreateObject ("Wscript.Shell")
Dim strArgs
strArgs = "cmd /c ai_model.bat"
oShell.Run strArgs, 0, false