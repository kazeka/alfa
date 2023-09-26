Создать работающий сервис на базе python + telegram bot + LLM local + finetune dataset

Подключенный к telegram-боту, работающий python-код (напр. aiogram, telegram.ext), использующий любую локальную LLM модель (без общеизвестных API, напр. ChatGPT, YandexGPT), способный вести диалог на русском языке.
Реализация должна включать finetuning model, например через парсинг общедоступной информации с сайта https://alfabank.by/

PS: полезные ссылки для выполнения ТЗ

https://betterprogramming.pub/private-llms-on-local-and-in-the-cloud-with-langchain-gpt4all-and-cerebrium-6dade79f45f6
https://github.com/imartinez/privateGPT
https://pub.towardsai.net/meta-releases-llama-2-free-for-commercial-use-e4662757e7d1
https://huggingface.co/datasets/
https://github.com/nomic-ai/gpt4all
https://the-eye.eu/public/AI/
https://gpt4all.io/index.html
https://medium.com/@kennethleungty/running-llama-2-on-cpu-inference-for-document-q-a-3d636037a3d8?source=email-b514a69ac1c5-1690070070505-digest.reader-7f60cf5620c9-3d636037a3d8----0-73------------------83e886a6_8f10_4ba6_82f6_da6c4318e741-1
Пример демонстрации диалога в ожидаемой реализации:
Запрос в tg: «Какую кредитную карту я могу оформить в Альфабанк Беларусь?»

Демонстрация без finetune-модели:
Ответ tg-бота: «Вы можете оформить карту Visa»

Демонстрация с использованием finetune-модели:
Ответ tg-бота: «Вы можете оформить “карту 100 дней” перейдя по ссылке https://www.alfabank.by/credits/cards/100-day/ »