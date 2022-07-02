---
layout: post
title:  "AWS LambdaでSelenium(Python) を使ってスクレイピング"
date:   2022-07-02
---

## やりたいこと

- AWS Lambda上で、Seleniumを使ってスクレイピング

## やったことのながれ

1. 技術要素の確認
2. ローカル開発環境の作成
3. ローカル開発環境での動作確認
4. AWS Lambda関数の作成/デプロイ -> エラー

## 技術要素の確認

- [Selenium Official](https://www.selenium.dev/)
  - [Getting started](https://www.selenium.dev/documentation/webdriver/getting_started/)
  - [Install a Selenium library](https://www.selenium.dev/documentation/webdriver/getting_started/install_library/)
  - [Three Ways to Use Drivers](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/#three-ways-to-use-drivers)
    - [1. Driver Management Software](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/#1-driver-management-software)
- [AWS Lambda](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/welcome.html)
  - [AWS Lambdaの基礎](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/lambda-foundation.html)
  - [Lambda ランタイム](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/lambda-runtimes.html)
  - [.zip ファイルアーカイブで Python Lambda 関数をデプロイする](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-package.html)

## ローカル開発環境の作成

### 自分の環境

```Markdown
M1チップMacBook Air
macOS Monterey 12.4
Python 3.9.12
PyCharm 2022.1.2(Community Edition)
```

### 追加でやったこと

```Bash
pip install selenium
pip install webdriver_manager
```

```Bash
pip list
selenium           4.3.0
webdriver-manager  3.7.1
```

## ローカル開発環境での動作確認

①以下コード実行して、

```Python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


service = ChromeService(executable_path=ChromeDriverManager(path=r"/tmp").install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.example.com/")
print(driver.title)
driver.quit()
```

②以下の出力を確認。（headlessモードなので、ブラウザGUI起動はなし）

```bash
[WDM] - ====== WebDriver manager ======

[WDM] - Current google-chrome version is 103.0.5060
[WDM] - Get LATEST chromedriver version for 103.0.5060 google-chrome
[WDM] - Driver [/tmp/.wdm/drivers/chromedriver/mac64/103.0.5060.53/chromedriver] found in cache
Example Domain
```

ここまでで、ローカルで、head-lessモードが動作することを確認

## AWS Lambda関数の作成/デプロイ

[.zip ファイルアーカイブで Python Lambda 関数をデプロイする](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-package.html)の手順に従い、関数をデプロイ

以下のエラーに ... chromedriverがstatus code 127でクラッシュしてる
```Bash
{
  "errorMessage": "Message: Service /tmp/.wdm/drivers/chromedriver/linux64/103.0.5060.53/chromedriver unexpectedly exited. Status code was: 127\n",
  "errorType": "WebDriverException",
  "stackTrace": [
    "  File \"/var/task/lambda_function.py\", line 10, in lambda_handler\n    driver = webdriver.Chrome(service=service, options=options)\n",
    "  File \"/var/task/selenium/webdriver/chrome/webdriver.py\", line 69, in __init__\n    super().__init__(DesiredCapabilities.CHROME['browserName'], \"goog\",\n",
    "  File \"/var/task/selenium/webdriver/chromium/webdriver.py\", line 89, in __init__\n    self.service.start()\n",
    "  File \"/var/task/selenium/webdriver/common/service.py\", line 98, in start\n    self.assert_process_still_running()\n",
    "  File \"/var/task/selenium/webdriver/common/service.py\", line 110, in assert_process_still_running\n    raise WebDriverException(\n"
  ]
}
```

[Stack Overflow: WebDriverException: Message: Service chromedriver unexpectedly exited. Status code was: 127](https://stackoverflow.com/questions/49323099/webdriverexception-message-service-chromedriver-unexpectedly-exited-status-co)
によると、いくつかOS側のライブラリがないと動かないらしい ... うーん厳しい。
