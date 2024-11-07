MAKEFLAGS += --silent
path := .
LOCAL_ENV := $(path)/.env.local

.PHONY: help lint clean test-message test-rss-feed build-image run-container run

## 관리용 커맨드
help: ## 지금 보고계신 도움말
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

lint: ## 코드 정리
	poetry run black .
	poetry run isort .

clean: ## 캐시 및 필요없는 리소스 제거
	rm -rf `find . -name '__pycache__'`
	rm -rf `find . -name '*.pyc'`
	rm -rf `find . -name '.DS_Store'`

## 작업용 커맨드
test-message: ## 테스트 메시지
	poetry run python -m scripts.google-chat 안녕하세요 from "make test-message"

test-rss-feed: ## 테스트 RSS 피드
	poetry run python -m scripts.get-rss-feed

build: ## 도커 이미지 빌드
	docker build -t rss-feed .

run: ## 도커 컨테이너 실행, 매번 다른 이름으로 실행, 볼륨 연결 (data:/app/data)
	docker run \
		-e GOOGLE_CHAT_KEY=${GOOGLE_CHAT_KEY} \
		-e GOOGLE_CHAT_TOKEN=${GOOGLE_CHAT_TOKEN} \
		--rm \
		-v `pwd`/web:/rss-follow-up/web \
		rss-feed \
		python -m main
