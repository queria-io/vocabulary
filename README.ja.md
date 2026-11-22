# vocabulary

[English](README.md)

日本のオープンデータの列に、共通の名前と意味を与えるための語彙。名前が違う列でも、
同じものを指していればここで結ぶ。Queria が最初の利用者だが、Queria 専用の仕様ではない。
国・自治体・企業の誰でも PR で提案できる。

## ファイル

- `entities.csv`: 実体の語彙。列が「何を識別するか」（都道府県・市区町村・地域メッシュ・法人など）。
  識別する実体が同じ列どうしは、名前やコードの形が違っても結合できる
- `data_elements.csv`: データ項目の語彙。列が「何を表すか」と、その標準の名前。
  ISO/IEC 11179 のデータ項目（data element）にあたる

例えば `prefecture_code`（都道府県コード）と `prefecture`（都道府県名）は別のデータ項目だが、
どちらも実体は `prefecture` を識別する。

## data_elements.csv の列

- `name`: 列名。日本の公的データで使う名前
- `title`: 日本語名。GIF の項目名、無ければ IMI の語
- `schema_org`: schema.org のプロパティ名
- `gif_class`・`gif_term`: GIF のクラスと英語名。GIF の URI は v2.4 時点で暫定なので組で指す
- `imi_term`: IMI コア語彙の語。URI は `http://imi.go.jp/ns/core/rdf#` に続けたもの
- `entity`: この項目が識別する実体（`entities.csv` の `name`）。識別に使わない項目は空
- `type`・`format`: 型と値の形
- `aliases`: 同じ項目を指す、ほかの列名（`;` 区切り）
- `note`: 判断の理由

## 名前の基準

- 一般のデータ（地図・施設・海外由来など）: schema.org の語を snake_case にする
- 日本の公的データ（自治体・国の統計や台帳）: GIF の英語名を snake_case にする。ただし GIF の
  語が schema.org の語に修飾を足しただけのとき（`latitudeOfRepresentativePoint`）は短い方を使う
- どの語彙にも無い項目は、複数のデータセットで使うときだけ語彙の欄を空にして足す

`lat` や `pref_code` のような既存の省略形は `aliases` に入れる。

## データセットからの使い方

Queria のデータセットでは、`*.table.yml` の列に次のように書く。

```yaml
- name: postal_code
  title: 郵便番号
  semantic: { role: entity, name: postal_code }
```

列名は、日本の公的データなら `data_elements.csv` の `name` に、一般のデータなら `schema_org` を snake_case にしたもの（空なら `name`）に揃える。`semantic.name` は `entities.csv` の `name` に揃える。詳しい規約は [docs.queria.io のデータセットの規約](https://docs.queria.io/publish/conventions)にある。

## 語彙の出典

- schema.org: [schema.org](https://schema.org/)（CC BY-SA 3.0）
- GIF: [digital-go-jp/GIF](https://github.com/digital-go-jp/GIF)（デジタル庁）
- IMI: [共通語彙基盤 コア語彙 2.4.2](https://imi.go.jp/core/core242/)（CC0 1.0）

これらの語彙は Queria に公開データセット（`schemaorg`・`gif`・`imi`）として載っていて、SQL で引ける。

## 検査

```bash
uv run scripts/check.py
```

実体名の重複、データ項目の `entity` が `entities.csv` にあること、GIF・schema.org の語が実在すること、
`name` がそれらの snake_case であること、`aliases` が重複しないことを確かめる。PR ごとに CI が回す。

## ライセンス

[CC0 1.0](LICENSE)。
