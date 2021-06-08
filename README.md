# cryptanalyst_bot
Telegram бот для анализа рынка криптовалют

### Демо бот
https://t.me/demo_cryptanalyst_bot

### Скриншот
![](https://i.imgur.com/5JBtHcx.png)


### Зависимости
* [Python 3.6 (или выше)](https://www.python.org/)

### Установка бота
1. Скачайте файлы проекта:
   ```bash
   git clone https://github.com/Forwall100/cryptanalyst_bot.git
   ```
   
2. Откройте созданую папку:
   ```bash
   cd cryptanalyst_bot
   ```

3. Установите сторонние зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Отредактируйте config.py, добавьте свои токены
* [Получить токен бота](https://t.me/BotFather)
* [Получить токен CoinMarketCap](https://coinmarketcap.com/api/)
* [Получить токен screenshotmachine](https://www.screenshotmachine.com/)
* [Получить токен EthScan](https://etherscan.io/)
* [Получить токен Taapi](https://taapi.io/)

5. Запустите бота
    ```bash
    python bot.py
    ```

### Возможности бота
```/price [тикер монеты]``` — текущая цена монеты

```/change [тикер монеты]``` — измененение цены монеты за 24 часа  

```/list``` — сводка о отслеживаемых монетах и информация о доминации BTC и ETH

```/add [тикер монеты]``` — добавить монету в список отслеживания  

```/remove [тикер монеты]``` — удалить монету из списка отслеживания  

```/bubbles``` - визуализация рынка за неделю на сайте [cryptobubbles](https://cryptobubbles.net/)

```/mood``` - настроение рынка на базе индикатора [Bitcoin Rainbow Price Chart](https://www.blockchaincenter.net/bitcoin-rainbow-chart/)

```/explorer [адресс BTC кошелька]``` - информация о кошельке и QR код  

```/altindex``` - [Индекс сезона альткоинов](https://www.blockchaincenter.net/altcoin-season-index/)

```/fear``` - [Индекс страха и жадности](https://alternative.me/crypto/fear-and-greed-index/)

```/gas``` - Цены на gas eth с сайта [etherscan](https://etherscan.io/gastracker)

```/signal [тикекр монеты] [промежуток времени h/d/w/m час/день/неделя/месяц соответственно]``` - Анализ рынка на основе торговых индикаторов с сайта [Taapi](https://taapi.io/)

```/advsignal``` - Полные результаты анализа рынка с указанием индикаторов

### TODO
- [ ] Переписать функции, использующие API coinmarketcap на API Coingecko, т.к. он не требует ключа 
- [X] Написать рекомендательную систему на основе индикаторов с сайта [taapi.io](https://taapi.io/)
- [ ] Добавить информацию о действииях grayscale
- [X] Добавить разные списки отслеживания для каждого пользователя
- [ ] Добавить ивенты с coindar
- [X] Добавить цены на gas с сайта [gasnow.org](https://www.gasnow.org/)
- [X] Добавить подсказки команд

### Поддержать автора:
#### На нормальный сервер для демо бота

* Bitcoin: bc1q0k0c95zctw3m0vqqye3qds23esuscchzpfl5re

* Ethereum: 0x3c396471d68AbF7F2f9F92c745F8eE9F8785C212

* DASH: XwXdpu1FhHmEteVE4CLaeeJbg3ZWpcNvCK

* Zcash: t1Ppg6BRYQFCoLy8ZrNctMeQ1Qv9pRE3j4b

* Monero: 477QnDRCae4MUsCwU6JYZqVCKoxTsWFUJDeDdTng61Md5ryzebSHZjM2RaD1996kvzWE59Whnp1LSbtGgevjDTWqLzCdzNC

* Litecoin: LcKvQbSeLzAm2Sc2yqpkiFs1su4nABR8LZ
