![image](https://user-images.githubusercontent.com/49960425/134746779-83f24049-74a6-4fbd-8dbc-85aed032b752.png)

Atividade para testar minhas habilidades em Python e Flask

## Iniciando

Instale as dependências deste template utilizando o [Pipenv](https://pipenv.pypa.io/en/latest/), com o seguinte comando:

```
pipenv install
```

Para subir este app em ambiente de desenvolvimento de acordo com o seu sistema operacional, execute:

- Para Linux

```
sh run.sh
```

- Para Windows

```
.\windows_run.ps1
```

Este template, está configurado para utilizar um banco sqlite em ambiente de dev, e o Postgres em ambiente de prod.

## Migrations

Caso você faça alguma alteração nas models, e queira executar uma migration, utilize o seguinte comando:

```
alembic revision --autogenerate -m "<nome da migration>"
```

Para aplicar manualmente as migrations geradas no passo anterior, utilize o comando:

```
alembic upgrade head
```
