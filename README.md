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

### TODO
- [ ] Написать рекомендательную систему на основе индикаторов с сайта [taapi.io](https://taapi.io/)
- [ ] Добавить информацию о действииях grayscale
- [X] Добавить разные списки отслеживания для каждого пользователя
- [ ] Добавить ивенты с coindar
- [X] Добавить цены на gas с сайта [gasnow.org](https://www.gasnow.org/)
- [X] Добавить подсказки команд
