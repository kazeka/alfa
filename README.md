## Build/Сборка

```bash
git submodule init
git submodule update
pip install -r privateGPT/requirements.txt
pip install -r requirements.txt
pip install pysqlite3-binary
echo -e "__import__('pysqlite3')\nimport sys\nsys.modules['sqlite3'] = sys.modules.pop('pysqlite3')\n$(cat /usr/local/python/3.10.8/lib/python3.10/site-packages/chromadb/__init__.py)" >  /usr/local/python/3.10.8/lib/python3.10/site-packages/chromadb/__init__.py 
rm privateGPT/source_documents/state_of_the_union.txt
cp data/reference.txt privateGPT/source_documents/
pushd privateGPT && python3 ingest.py && popd
ln -s privateGPT/db
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q4_0.bin
mv llama-2-7b-chat.ggmlv3.q4_0.bin models/
python3 src/tbot.py

```


## Description/Описание

Connected to a telegram bot, running python code (eg aiogram, telegram.ext), using any local LLM model (without well-known APIs, eg ChatGPT, YandexGPT), capable of conducting a dialogue in Russian.
The implementation must include a finetuning model, for example, through parsing publicly available information from the site https://alfabank.by/

Создать работающий сервис на базе python + telegram bot + LLM local + finetune dataset

Подключенный к telegram-боту, работающий python-код (напр. aiogram, telegram.ext), использующий любую локальную LLM модель (без общеизвестных API, напр. ChatGPT, YandexGPT), способный вести диалог на русском языке.
Реализация должна включать finetuning model, например через парсинг общедоступной информации с сайта https://alfabank.by/

Создать работающий сервис на базе python + telegram bot + LLM local + finetune dataset

Подключенный к telegram-боту, работающий python-код (напр. aiogram, telegram.ext), использующий любую локальную LLM модель (без общеизвестных API, напр. ChatGPT, YandexGPT), способный вести диалог на русском языке.
Реализация должна включать finetuning model, например через парсинг общедоступной информации с сайта https://alfabank.by/

PS: полезные ссылки для выполнения ТЗ

1. https://betterprogramming.pub/private-llms-on-local-and-in-the-cloud-with-langchain-gpt4all-and-cerebrium-6dade79f45f6
1. https://github.com/imartinez/privateGPT
1. https://pub.towardsai.net/meta-releases-llama-2-free-for-commercial-use-e4662757e7d1
1. https://huggingface.co/datasets/
1. https://github.com/nomic-ai/gpt4all
1. https://the-eye.eu/public/AI/
1. https://gpt4all.io/index.html
1. https://medium.com/@kennethleungty/running-llama-2-on-cpu-inference-for-document-q-a-3d636037a3d8?source=email-b514a69ac1c5-1690070070505-digest.reader-7f60cf5620c9-3d636037a3d8----0-73------------------83e886a6_8f10_4ba6_82f6_da6c4318e741-1
1. https://archive.li/EJTp0

Пример демонстрации диалога в ожидаемой реализации:
Запрос в tg: «Какую кредитную карту я могу оформить в Альфабанк Беларусь?»

Демонстрация без finetune-модели:
Ответ tg-бота: «Вы можете оформить карту Visa»

Демонстрация с использованием finetune-модели:
Ответ tg-бота: «Вы можете оформить “карту 100 дней” перейдя по ссылке https://www.alfabank.by/credits/cards/100-day/ »