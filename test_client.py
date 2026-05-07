import httpx
import json

BASE_URL = "http://localhost:8000"


def print_response(response):
    """Красивый вывод ответа"""
    print(f"\n--- {response.request.method} {response.url} ---")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)


async def main():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:

        # 1. СОЗДАНИЕ объявления
        print("\n>>> 1. Создаем объявление...")
        ad_data = {
            "title": "Велосипед горный",
            "description": "Почти новый, 21 скорость",
            "price": 15000.0,
            "author": "Алексей"
        }
        response = await client.post("/advertisement", json=ad_data)
        print_response(response)

        if response.status_code != 200:
            print("Ошибка при создании!")
            return

        ad_id = response.json()["id"]
        print(f"\n>>> ID созданного объявления: {ad_id}")

        # 1.1 ПРОВЕРКА ВАЛИДАЦИИ: отрицательная цена (должна вернуть 422)
        print("\n>>> 1.1. Проверяем валидацию: пробуем создать с отрицательной ценой...")
        invalid_data = {
            "title": "Невалидное",
            "description": "Должно отклониться",
            "price": -500.0,
            "author": "Тестер"
        }
        response = await client.post("/advertisement", json=invalid_data)
        print_response(response)
        if response.status_code == 422:
            print("✅ Ошибка валидации: отрицательная цена отклонена (422)")
        else:
            print(f"❌ Ожидался 422, получен {response.status_code}")

        # 2. ПОЛУЧЕНИЕ по ID
        print(f"\n>>> 2. Получаем объявление с ID {ad_id}...")
        response = await client.get(f"/advertisement/{ad_id}")
        print_response(response)

        # 3. ОБНОВЛЕНИЕ (PATCH)
        print(f"\n>>> 3. Обновляем цену и описание...")
        update_data = {
            "price": 12000.0,
            "description": "Срочная продажа!"
        }
        response = await client.patch(f"/advertisement/{ad_id}", json=update_data)
        print_response(response)

        # 4. ПОИСК (GET с параметрами)
        print(f"\n>>> 4. Ищем объявления по слову 'Велосипед'...")
        response = await client.get("/advertisement", params={"title": "Велосипед"})
        print_response(response)

        # 4.1 ПОИСК по автору
        print(f"\n>>> 4.1. Ищем объявления по автору 'Алексей'...")
        response = await client.get("/advertisement", params={"author": "Алексей"})
        print_response(response)

        # 5. УДАЛЕНИЕ
        print(f"\n>>> 5. Удаляем объявление с ID {ad_id}...")
        response = await client.delete(f"/advertisement/{ad_id}")
        print_response(response)

        # Проверка, что удалилось
        print(f"\n>>> 6. Проверяем, что объявления больше нет...")
        response = await client.get(f"/advertisement/{ad_id}")
        print_response(response)
        if response.status_code == 404:
            print("\n✅ Всё отлично! Объявление успешно удалено.")
        else:
            print("\n❌ Ошибка: объявление не удалилось или найдено снова.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())