@echo off
SET CMD=%1

IF "%CMD%"=="test" (
	echo Executando testes...
	pytest tests -v
	goto end
)

IF "%CMD%"=="lint" (
	echo Executando linter ruff...
	ruff check --fix .
	goto end
)

IF "%CMD%"=="format" (
	echo Formatando o código com black...
	black mtcli_trade tests
    goto end
)

IF "%CMD%"=="check" (
	echo Verificando com ruff e black...
	ruff check .
	black --check .
	goto end
)

if "%cmd%" == "typecheck" (
	echo Verificando com mypy
	mypy mtcli_trade tests
	goto end
)


echo Comando invalido: %CMD%
echo "Uso: make [test | lint | format | check | typecheck]"

:end
