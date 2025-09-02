@echo off
SET CMD=%1

IF /i "%CMD%"=="test" (
	echo Executando testes...
	poetry run pytest --cov=mtcli_trade --cov-report=html -ra -q
	goto end
)

IF /i "%CMD%"=="lint" (
	echo Executando linter ruff...
	poetry run ruff check --fix .
	goto end
)

IF /i "%CMD%"=="format" (
	echo Formatando o codigo com black...
	poetry run black mtcli_trade tests
    goto end
)

IF "%CMD%"=="check" (
	echo Verificando com ruff e black...
	poetry run ruff check .
	poetry run black --check .
	goto end
)

if "%cmd%" == "typecheck" (
	echo Verificando com mypy
	poetry run mypy mtcli_trade tests
	goto end
)

echo Comando invalido: %CMD%
echo Uso: make [test] [lint] [format] [check] [typecheck]

:end
