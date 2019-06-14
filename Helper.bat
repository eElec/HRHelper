@ECHO off

SET ProgramType=%1
SET ProgramName=%2
SET ProgramPath="%3"

CD %ProgramPath%
IF %ERRORLEVEL% NEQ 0 GOTO:eof

IF /I %ProgramType%==py (
	GOTO pythonFunc
	
)
IF /I %ProgramType%==C++ (
	GOTO cppFunc
)

GOTO:eof

:cppFunc
g++ %ProgramName%.cpp -o %ProgramName%.exe
IF %ERRORLEVEL% NEQ 0 goto:eof
%ProgramName%.exe < inp.txt > output.txt
FC out.txt output.txt /W
IF %ERRORLEVEL% EQU 0 echo Correct Output 
type output.txt
echo
GOTO:eof

:pythonFunc
python %ProgramName%.py < inp.txt > output.txt
GOTO:eof