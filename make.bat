@echo off
SET CMD=%1

IF /i "%CMD%"=="test" (
	echo Executando testes...
	poetry run pytest --cov=mtcli_trade --cov-report=html
	goto :EOF
)

IF /i "%CMD%"=="format" (
	echo Formatando o codigo com black...
	poetry run black .
    goto :EOF
)

IF "%CMD%"=="check" (
	echo Verificando o codigo com black...
	poetry run black --check .
	goto :EOF
)

echo Comando invalido: %CMD%
echo Uso: make [test] [format] [check]
