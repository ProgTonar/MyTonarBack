import os
import typer
import inflect

app = typer.Typer()
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # корень
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app'))  # из корня в нужную папку
p = inflect.engine()

def pluralize(name: str) -> str:
    return p.plural(name)

# Функция создания папки с __init__.py
def create_folder_with_init(path, is_database=False):
    os.makedirs(path, exist_ok=True)
    init_path = os.path.join(path, '__init__.py')
    if not os.path.exists(init_path):
        with open(init_path, 'w') as f:
            if is_database:
                # Для database автоматически подключаем базовые объекты
                f.write("from .database import SessionLocal, engine, Base\n")
            else:
                f.write("# init file\n")

def create_git_ignore(path):
    os.makedirs(path, exist_ok=True)
    ignore_path = os.path.join(path, '.gitignore')
    if not os.path.exists(ignore_path):
        with open(ignore_path, "w") as f:
            f.write(
                "/__pycache__\n"
            )

# Проверка на существование файла
def check_file_exists(file_path):
    if os.path.exists(file_path):
        typer.echo(f"❌ Файл уже существует: {file_path}")
        raise typer.Exit()

# Команда создания структуры проекта
@app.command()
def make_project():
    folders = ["models", "schemas", "routes", "service", "database", "storage"]
    for folder in folders:
        path = os.path.join(BASE_DIR, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            typer.echo(f"✅ Папка {folder} создана")
            create_folder_with_init(path, is_database=(folder == "database"))
            create_git_ignore(path)
        else:
            typer.echo(f"⚠️ Папка {folder} уже существует")

    # Создание файла базы данных
    db_file = os.path.join(BASE_DIR, "database", "database.py")
    if not os.path.exists(db_file):
        with open(db_file, "w") as f:
            f.write(
                "from sqlalchemy import create_engine\n"
                "from sqlalchemy.orm import declarative_base\n"
                "from sqlalchemy.orm import sessionmaker\n\n"
                "SQLALCHEMY_DATABASE_URL = 'sqlite:///./database/base.db'\n\n"
                "engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={\"check_same_thread\": False})\n"
                "SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)\n"
                "Base = declarative_base()\n"
            )
        typer.echo("✅ Файл database.py создан")
    else:
        typer.echo("⚠️ Файл database.py уже существует")

    main = os.path.join(BASE_DIR, "main.py")
    if not os.path.exists(main):
        with open(main, "w") as f:
            f.write(
                'from fastapi import FastAPI\n'
                'from fastapi.staticfiles import StaticFiles\n'
                'from database import Base, engine\n\n'
                'app = FastAPI()\n\n'
                '# Создание таблиц\n'
                'Base.metadata.create_all(bind=engine)\n\n'
                '# Монтируем папку со статическимим файлами\n'
                'app.mount("/files", StaticFiles(directory="storage/files"), name="files")\n\n'
                '# Подключаем роуты\n'
                'app.include_router(Rout.router, prefix="/path_name", tags=["User"])\n\n'
                '@app.get("/")\n'
                'async def root():\n'
                '    return {"message": "Hello World!"}\n'
            )
        typer.echo("✅ Файл main.py создан")
    else:
        typer.echo("⚠️ Файл main.py уже существует")

    create_git_ignore(BASE_DIR)

# Команда создания модели
@app.command()
def make_model(name: str):
    path = os.path.join(BASE_DIR, "models")
    create_folder_with_init(path)
    file_path = os.path.join(path, f"{pluralize(name)}.py")
    check_file_exists(file_path)
    create_git_ignore(path)

    with open(file_path, "w") as f:
        f.write(
            "from database import Base\n"
            "from sqlalchemy import Column, Integer, String\n"
            "from sqlalchemy.orm import relationship\n\n"
            f"class {pluralize(name)}(Base):\n"
            f"    __tablename__ = '{pluralize(name.lower())}'\n\n"
            f"    id = Column(Integer, primary_key=True, index=True)\n"
            f"    name = Column(String, index=True)\n"
        )
    typer.echo(f"✅ Модель {name} создана")

# Команда создания схемы
@app.command()
def make_schema(name: str):
    path = os.path.join(BASE_DIR, "schemas")
    create_folder_with_init(path)
    file_path = os.path.join(path, f"{name}Schema.py")
    check_file_exists(file_path)
    create_git_ignore(path)

    with open(file_path, "w") as f:
        f.write(
            "from pydantic import BaseModel, Field\n"
            "from typing import Optional\n\n"
            f"class {name}Schema(BaseModel):\n"
            f"    name: str\n"
        )
    typer.echo(f"✅ Схема {name} создана")

# Команда создания роутера
@app.command()
def make_route(name: str):
    path = os.path.join(BASE_DIR, "routes")
    create_folder_with_init(path)
    file_path = os.path.join(path, f"{name}Route.py")
    check_file_exists(file_path)
    create_git_ignore(path)

    with open(file_path, "w") as f:
        f.write(
            "from fastapi import APIRouter, Depends\n\n"
            "from database import get_db\n"
            "from sqlalchemy.orm import Session\n"
            f"from service.{name}Service import {name}Service\n\n"
            "router = APIRouter()\n\n"
            f"def get_{name.lower()}_service(db: Session = Depends(get_db)):\n"
            f"  return {name}Service(db)\n\n"
            f"# @router.get('/{name.lower()}')\n"
            f"# async def create_{name.lower()}({name.lower()}: {name}Create, service: {name}Service = Depends(get_{name.lower()}_service)):\n"
            f"# return {{'message': 'Это роут {name}'}}\n"
        )
    typer.echo(f"✅ Путь {name} создан")

# Команда создания сервиса
@app.command()
def make_service(name: str):
    path = os.path.join(BASE_DIR, "service")
    create_folder_with_init(path)
    file_path = os.path.join(path, f"{name}Service.py")
    check_file_exists(file_path)
    create_git_ignore(path)

    with open(file_path, "w") as f:
        f.write(
            f"from sqlalchemy.orm import Session\n\n"
            f"class {name}Service:\n"
            f"    def __init__(self, db: Session):\n"
            f"        self.db = db\n\n"
            f"    def example_method(self):\n"
            f"        return 'Hello from {name}'\n"
        )
    typer.echo(f"✅ Сервис {name} создан")

@app.command()
def make_util(name: str):
    path = os.path.join(BASE_DIR, "utils")
    create_folder_with_init(path)
    file_path = os.path.join(path, f"{name}Util.py")
    check_file_exists(file_path)
    create_git_ignore(path)

    with open(file_path, "w") as f:
        f.write(
            f"# Util {name}"
        )
    typer.echo(f"✅ Утилита {name} создана")

@app.command()
def make_test(name: str):
    path = os.path.join(BASE_DIR, "tests")
    create_folder_with_init(path)
    file_path = os.path.join(path, f"test_{name}.py")
    check_file_exists(file_path)
    create_git_ignore(path)

    with open(file_path, "w") as f:
        f.write(
            "import pytest\n"
            "from httpx import AsyncClient, ASGITransport\n"
            "from main import app\n\n"
            "transport = ASGITransport(app=app)\n"
            "base_url = \"http://test\"\n\n"
            "@pytest.mark.asyncio\n"
            "async def test_create_user_success():\n"
            "    async with AsyncClient(transport=transport, base_url=base_url) as ac:\n"
            "        response = await ac.post(\"/user/create\", json={\n"
            "            \"name\": \"Тест\",\n"
            "            \"email\": \"newuser@example.com\"\n"
            "        })\n"
            "    assert response.status_code == 200\n"
            "    assert \"успешно\" in response.text\n\n"
            "@pytest.mark.asyncio\n"
            "async def test_create_user_invalid_email():\n"
            "    async with AsyncClient(transport=transport, base_url=base_url) as ac:\n"
            "        response = await ac.post(\"/user/create\", json={\n"
            "            \"name\": \"Тест\",\n"
            "            \"email\": \"notanemail\"\n"
            "        })\n"
            "    assert response.status_code == 422\n\n"
            "# @pytest.mark.asyncio\n"
            "# async def test_upload_avatar_without_token():\n"
            "#    async with AsyncClient(transport=transport, base_url=base_url) as ac:\n"
            "#        with open(\"tests/test_image.jpg\", \"rb\") as file:\n"
            "#            files = {\"file\": (\"test.jpg\", file, \"image/jpeg\")}\n"
            "#            response = await ac.post(\"/user/1/upload_avatar\", files=files)\n"
            "#    assert response.status_code == 401\n"
            "#    assert \"Требуется токен\" in response.text\n"
        )

    typer.echo(f"✅ Тест {name} создан")

# Запуск CLI
if __name__ == "__main__":
    app()