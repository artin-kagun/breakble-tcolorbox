# nested breakable tcolorbox 要件整理

作成日: 2026-05-24

## 目的

このプロジェクトでは、`tcolorbox` の元機能を壊さずに、`breakable`
な `tcolorbox` の中にさらに `breakable` な `tcolorbox` を置いた場合でも、
内側の箱が自然にページをまたげる版を作る。

ただし、これは「見た目が似ていればよい」修正ではない。
入れ子ではない通常利用については、元の `tcolorbox` と寸分違わない出力を維持する。
その上で、入れ子の `breakable` について、元実装でできなかったページ跨ぎを追加する。

## 最重要要件

### 1. 入れ子なしでは、通常の `tcolorbox` と完全一致する

改造版は、入れ子 `breakable` を実装した後でも、入れ子ではない
`breakable` 箱については、元の `tcolorbox` と同じ入力に対して、
同じページ、同じ高さ、同じ行位置、同じ描画で分割されなければならない。

検証では、元の `tcolorbox` と改造版 `tcolorbox` に同一の `.tex` を読ませ、
生成された PDF をページごとに画像化し、pixel 単位で一致することを確認する。

この比較対象には、少なくとも以下を含める。

- 通常の `breakable`
- `title after break`
- `adjusted title after break`
- `break at`
- `pad before break`, `pad after break`, `pad at break`
- `toprule at break`, `bottomrule at break`
- `height fixed for`
- `vfill before first`
- `tcblower` と segmentation
- `extras first`, `extras middle`, `extras last`
- `overlay unbroken`, `overlay first`, `overlay middle`, `overlay last`
- `underlay unbroken`, `underlay first`, `underlay middle`, `underlay last`

### 2. 入れ子ではない機能は完全互換にする

改造版は、入れ子 `breakable` の修正以外で元の `tcolorbox` の挙動を変えてはならない。

特に、以下は元実装と同一である必要がある。

- 箱の高さ計算
- ページブレイク位置
- frame, interior, title, segmentation の描画
- `first`, `middle`, `last`, `unbroken` の状態判定
- overlay / underlay / extras の実行タイミング
- listing, theorem, raster, fitting, skins など主要ライブラリ利用時の見た目
- 警告、エラー、overfull / underfull の発生状況

### 3. 入れ子 `breakable` は、通常の `breakable` と同じくらいページ下部まで到達する

`breakable` な外側の箱の中に `breakable` な内側の箱がある場合でも、
通常の入れ子なし `breakable` と比べて、ページ下部への到達度合いが悪くなってはいけない。

つまり、入れ子にしたせいで、本来ならまだ本文を置けるはずのページ下部が
大きく空いてしまう実装は失敗とする。

比較の考え方は以下。

- 同じ A4 ページ、同じ余白、同じ本文量で、入れ子なしの通常 `breakable` を作る。
- それと対応する入れ子 `breakable` 版を作る。
- 各ページで、箱の背景・左右罫線・本文がどの高さまで届いているかを見る。
- 入れ子版だけが明らかに早い位置で切れて、ページ下部に大きな余白を残す場合は不合格。
- 通常版で下部まで到達できる状況では、入れ子版も同程度まで到達する必要がある。

期待する挙動は、次のように言語化する。

- 内側の箱は、そのページで入るところまで描画される。
- ページ末尾では、内側の箱の背景と左右罫線が、本文が存在する位置まで自然に続く。
- 次ページ先頭では、内側の箱の続きが、通常の `tcolorbox` の続きと同じように始まる。
- 次ページ先頭に、前ページで使い切れなかった高さ由来の大きな空白が出てはいけない。
- 入れ子を複数段にしても、各段の先頭空白が累積して、本文がページの途中からしか出ない状態になってはいけない。
- 入れ子にしたせいで、ページ末尾の本文到達位置が通常の非入れ子 `breakable`
  より目に見えて上がってはいけない。多段入れ子でも「安全のために早く切る」実装を
  合格にしない。
- `title after break` / `adjusted title after break` があるケースだけで成立してはいけない。
  continuation title を出さず、普通の文章の途中から次ページへ続くケースも必須とする。
- `notitle` の箱、タイトルはあるが continuation title は出さない箱、4段以上の多段入れ子も
  検証対象に含める。
- A4 固定にしない。`letterpaper`、B5、任意の `paperwidth` / `paperheight` / margin でも、
  紙面寸法をハードコードせず現在の紙面・本文領域から計算する。

言い換えると、内側の箱の continuation fragment は、親 fragment の中で
「余った高さを持ち越した箱」ではなく、「そのページの先頭から普通に続く箱」
として扱われる必要がある。

さらに、ここで禁止する「内側に入る」は横方向ではなく高さ方向の現象を指す。
入れ子にした結果、左右の余白や枠線ぶん横幅が狭くなるのは自然な挙動である。
一方で、改ページ直前・直後に、入れ子の深さに比例して本文を置ける縦方向の領域が
削られる挙動は失敗とする。

具体的には、入れ子の各段が「安全のための余白」や「見えない予約高さ」を持ち寄って、
最内側の本文がページ下部まで到達しなくなる実装を合格にしない。ページ末尾で必要なのは、
実際に描画される frame / title / rule / boxsep / top / bottom / break sep だけを差し引いた
残り領域に本文が入ることであり、入れ子段数そのものを理由に本文収容量を減らしてはいけない。

この要件を検証するため、入れ子深度 0, 1, 2, 3, 4 以上のサンプルを用意し、
各深度の最初の break fragment で「ページ下端から最後の本文・背景・罫線までの距離」を比較する。
深い入れ子だけが段数に応じて早く切れている場合は不合格とする。

### 3.1 横並び目視比較 PDF を必須成果物にする

機械的な pixel 比較だけではなく、人間が疑わしい余白を一目で見られる PDF を必ず生成する。

- 左ページまたは左カラムに、改造していない本物の `tcolorbox` の出力を置く。
- 右ページまたは右カラムに、改良版 `tcolorbox` の出力を置く。
- 入れ子なし比較では、左右が完全に同じ見た目であることを確認する。
- 入れ子あり比較では、本物 `tcolorbox` は入れ子 breakable 非対応の参照として置き、
  改良版が「ページ下部まで自然に本文が流れる」ことを確認する。
- 比較 PDF は A4 のサンプルを元に作る。

### 3.2 普通の文章継続を主検証ケースにする

`title after break` や `adjusted title after break` は重要な機能だが、それだけを検証してはいけない。
主検証では、改ページ後が continuation title から始まるケースだけでなく、
普通の文章の途中からそのまま次ページへ続くケースを必ず含める。

必須ケースは以下。

- 入れ子なしで長文を書いた通常の `breakable`。
- 1段入れ子で、内側 box の本文が普通の文章として複数ページに続くケース。
- 2段、3段、4段以上の入れ子で、最内側 box の本文が普通の文章として続くケース。
- 外側 box がページ途中から始まり、その残りページに内側 box の先頭本文が入るケース。
- タイトルなし `notitle` の内側 box。
- タイトルはあるが continuation title を出さない内側 box。
- `title after break` / `adjusted title after break` を使う内側 box。

### 4. 入れ子の break 境界でも `first/middle/last` 系機能が正しく動く

内側の箱がページをまたぐ場合でも、元の `tcolorbox` が通常 breakable で持つ
fragment 状態は保存される必要がある。

具体的には、以下が正しく機能すること。

- 最初の fragment では `first` 用の frame/interior/title/overlay/underlay/extras が使われる。
- 中間 fragment では `middle` 用の frame/interior/title/overlay/underlay/extras が使われる。
- 最後の fragment では `last` 用の frame/interior/title/overlay/underlay/extras が使われる。
- 分割されない場合は `unbroken` として扱われる。
- `title after break` は continuation fragment の先頭に出る。
- `tcblower` を含む上下分割でも segmentation が欠けたり重なったりしない。

### 5. 補助描画でごまかさない

継ぎ目を隠すために、frame や background を大きく伸ばしてはいけない。
そのような実装は、同じページ上に fragment が並んだ場合に本文を覆ったり、
罫線が太くぼけたりする。

必要なのは、描画を後から塗り足すことではなく、元の `tcolorbox` と同じ
fragment 高さ計算・同じ状態遷移・同じ描画手順で、親箱のページ分割に参加できること。

## ディレクトリ構成要件

検証しやすくするため、元実装と改造実装を明確に分ける。

- `vendor/tcolorbox-original/`
  - CTAN または TeX Live から持ってきた、改造していない本物の `tcolorbox`
- `work/tcolorbox-patched/`
  - 編集対象の `tcolorbox`
- `tests/a4/`
  - A4 用の、人間が読みやすいサンプル
- `tests/compare/`
  - 元実装と改造版に同じ `.tex` を読ませる pixel 比較用サンプル
  - ここも原則 A4 とする
- `build/compare/original/`
  - 元実装で生成した PDF と画像
- `build/compare/patched/`
  - 改造版で生成した PDF と画像
- `build/compare/diff/`
  - 差分画像、比較レポート

## サンプルファイル要件

サンプルは A4 を基本にする。
比較用サンプルも A4 で作る。
テストのために極端な小型ページを使う場合も、A4 サンプルとは別ファイルに分け、
主たる合否判定には使わない。

A4 サンプルには以下を含める。

- 通常の文章が多く入った箱
- 入れ子なしの通常 `breakable`
- 1段入れ子の `breakable`
- 2段以上の入れ子 `breakable`
- 入れ子なし通常版と入れ子版のページ下部到達度を見比べるケース
- `title after break` あり
- `underlay/overlay` の `unbroken/first/middle/last`
- `extras first/middle/last`
- `tcblower` と segmentation
- `break at`, `pad at break`, `height fixed for`
- listing, theorem, raster, fitting, skins の代表例

サンプルの目的は「それっぽい絵を作ること」ではなく、どのページのどの fragment が
どの状態で描かれているかを人間が追えるようにすること。

## 検証要件

### pixel 一致テスト

元実装と改造版で同一 `.tex` をコンパイルし、PDF を同じ解像度の PNG に変換して比較する。

入れ子でないケースは、全ページ pixel 一致を必須とする。

### 入れ子専用テスト

元実装では期待出力を作れないため、以下をチェックする。

- ページ先頭に不自然な空白がない。
- ページ末尾に本文があるところまで箱が自然に続く。
- 入れ子なし通常 `breakable` と比べて、入れ子版だけページ下部への到達が明らかに悪くならない。
- frame/interior/title/segmentation が欠けない。
- overlay/underlay/extras の `first/middle/last` が期待 fragment に出る。
- 入れ子を深くしても、先頭空白が累積しない。
- ログに LaTeX error, package warning, overfull, underfull が出ない。

### 目視確認 PDF

pixel 比較の機械テストとは別に、以下の PDF を作る。

- 元実装だけの出力
- 改造版だけの出力
- 元実装と改造版を同じページ順で見比べられる比較 PDF
- 入れ子 `breakable` 専用の期待挙動確認 PDF

## 合意済みの方針

- 実装方法は、利用者側がアルゴリズムを指定するものではない。
  要件を満たす一番よい方法を実装側で選ぶ。
- 目的は「入れ子ありの `breakable` を実装し、その副作用として入れ子なしの通常利用が
  元実装から一切変わらないこと」を確認すること。
- 比較用サンプルも A4 で作る。
- 入れ子にしたとき、通常の `breakable` よりページ下部まで行けなくなる問題を
  必ず回避する。

## 次に作るもの

1. 本物の `tcolorbox` を `vendor/tcolorbox-original/` に置く。
2. 編集対象を `work/tcolorbox-patched/` に分ける。
3. A4 の比較用 `.tex` を作る。
4. 同一 `.tex` を元実装・改造版でコンパイルし、PDF と PNG を生成する。
5. 入れ子なしケースは pixel 完全一致を合格条件にする。
6. 入れ子ありケースは、ページ上部の不自然な空白、ページ下部到達度、
   `first/middle/last/unbroken` 系描画を合格条件として見る。
