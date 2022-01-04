---
layout: post
title:  "GitHubPagesでカスタムThemeのJekyll"
date:   2022-01-04 22:53:04 +0900
---

# やったこと

- GitHub PagesでJekyllのthemeを上書きして最低限の装飾ページを作成 

# メモ

## Ruby

- rbenv
  - Rubyバージョン切り替えツール、venv的な
- Rubyのライブラリ管理
  - gem(ライブラリ自体を示したり、コマンドだったり)
  - rubygems(パッケージ管理全体)
  - bundler(Gemfileはこちら、pipfile的な)

## GitHub Pages

- デフォルトは、Jekyllでサイトレイアウトしてくれる
  - themeを上書きするときは、_layoutsを自作
  - Jekyllを無効化したいときは、.nojekyll


# 参考サイト

- http://jekyllrb-ja.github.io/docs/themes/
- https://zenn.dev/osuzuki/articles/a535b2840bbea3