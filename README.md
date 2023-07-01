# Technos Cal NetworkAddress Tool

## 依存関係
- Python3
- pip3

## deploy
```bash
git clone git@github.com:chouett0/calc-netaddr.git
cd calc-netaddr
docker build -t webapp .
docker run -d --rm -p 5000:5000 --name webapp webapp
```
URL: http://[ホスト端末のIPアドレス]:5000/calcaddr/calc

## How to Use
```bash
export secret_key=[ランダムな値] && openai_key=[OpenAI API KEY] && flask run -h 0.0.0.0
```
