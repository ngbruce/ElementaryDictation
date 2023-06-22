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
echo ------------------------------
echo - 4 - fetch --all
echo - 5 - pull origin master
echo ------------------------------
echo - 6 - status
echo - 7 - log
echo ------------------------------
echo - 8 - set proxy
echo - 9 - unset proxy
echo ------------------------------
echo - s - view global settings
echo ------------------------------
echo - 0 - 返回
echo ------------------------------
set "gitsel=x"
set /p "gitsel=请选择操作: "
if %gitsel%==1 (
    git add .
	echo ------------------------------
    echo add执行完毕，按任意键返回
    pause
	goto start_git
) else if %gitsel%==2 (
    set /p "cname=请输入commit注释: "
    git commit -m "!cname!"
	echo ------------------------------
    echo -commit- 执行完毕，按任意键返回
    pause
    goto start_git
) else if %gitsel%==3 (
	git push origin master
	echo ------------------------------
	echo - push- 执行完毕，按任意键返回
	pause
	goto start_git
rem	exit
) else if %gitsel%==4 (
	git fetch --all
	echo ------------------------------
	echo - fetch -all- 执行完毕，按任意键返回
	pause
	goto start_git
) else if %gitsel%==5 (
	git pull origin master
	echo ------------------------------
	echo - pull- 执行完毕，按任意键返回
	pause
	goto start_git
) else if %gitsel%==6 (
	git status
	echo ------------------------------
	echo - status- 执行完毕，按任意键返回
	pause
	goto start_git
) else if %gitsel%==7 (
	git log
	echo ------------------------------
	echo - log- 执行完毕，按任意键返回
	pause
	goto start_git
) else if %gitsel%==8 (
	git config --global http.proxy http://127.0.0.1:10809
	git config --global https.proxy http://127.0.0.1:10809
	git config --global socks.proxy socks5://127.0.0.1:10808
	echo ------------------------------
	git config --global --list
	echo ------------------------------
	echo - set proxy- 执行完毕，按任意键返回
	pause
	goto start_git
) else if %gitsel%==9 (
	git config --global --unset http.proxy
	git config --global --unset https.proxy
	git config --global --unset socks.proxy
	echo ------------------------------
	git config --global --list
	echo ------------------------------
	echo - unset proxy- 执行完毕，按任意键返回
	pause
	goto start_git
) else if %gitsel%==s (
	git config --global --list
	echo ------------------------------
	echo - view- 执行完毕，按任意键返回
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
