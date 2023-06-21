chcp 65001
@echo off
title git工具
:start_git
setlocal enabledelayedexpansion
cls
rem set /p "test=请输入commit注释: "
rem echo 输入的名称是：%test%
echo 选择功能
echo ------------------------------
echo - 1 - add.
echo - 2 - commit -m ...
echo - 3 - push origin master
echo - 4 - fetch --all
echo - 5 - pull origin master
echo - 6 - status
echo - 7 - log
echo ------------------------------
echo - 0 - 返回
echo ------------------------------
set "gitsel=x"
set /p "gitsel=请选择操作: "
if %gitsel%==1 (
    git add .
    echo add执行完毕，按任意键返回
    pause
	goto start_git
) else if %gitsel%==2 (
    set /p "cname=请输入commit注释: "
    git commit -m "!cname!"
    echo -commit- 执行完毕，按任意键返回
    pause
    goto start_git
) else if %gitsel%==3 (
	git push origin master
	echo - push- 执行完毕，按任意键返回
	pause
	goto start_git
rem	exit
) else if %gitsel%==4 (
	git fetch --all
	echo - fetch -all- 执行完毕，按任意键返回
	pause
	goto start_git
) else if %gitsel%==5 (
	git pull origin master
	echo - pull- 执行完毕，按任意键返回
	pause
	goto start_git
) else if %gitsel%==6 (
	git status
	echo - status- 执行完毕，按任意键返回
	pause
	goto start_git
) else if %gitsel%==7 (
	git log
	echo - log- 执行完毕，按任意键返回
	pause
	goto start_git
) else if %gitsel%==0 (
	goto end
) else (
	cls
    echo 输入有误,请重新输入!
    pause
    goto start_git
)
:end
