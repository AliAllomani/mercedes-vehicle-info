# Mercedes-Benz Vehicle Information

## Developer Account

Via [https://developer.mercedes-benz.com/]

## Env Setup

Create `.env` file with the following vars

```bash
MB_CLIENT_ID=xxx-xxx-xxx-xxx-xxxx
MB_CLIENT_SECRET="xxxxxxx"
MB_VIN=WDDxxxxxxxx
MB_REDIRECT_URL="https://localhost:3000/callback"
MB_IS_DEMO="false"
```

## Test

```bash
pipenv install
pipenv run python ./main.py
```
