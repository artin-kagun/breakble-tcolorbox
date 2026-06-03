# breakble-tcolorbox

[English](README.md) | [日本語](README.ja.md)

`breakble-tcolorbox` は
[`tcolorbox`](https://github.com/T-F-S/tcolorbox) 6.10.0 をベースにした、非公式の改変版です。

公開されている `tcolorbox` の使い方との互換性を保ちながら、入れ子になった `breakable` ボックスのページ分割を改善するためのパッケージです。親の `tcolorbox` が `breakable` のとき、その中に入れた通常の `breakable` な `tcolorbox` も、親のページ分割の流れに沿って自然に分割できるようにします。

このパッケージで大切にしていることは次のとおりです。

- 入れ子ではない通常の `tcolorbox` の出力は、元の `tcolorbox` と同じにする。
- upstream のサンプルやマニュアルソースの出力も、元の `tcolorbox` と同じに保つ。
- `breakable` なボックスの中に長い `breakable` ボックスを入れたとき、内側のボックスが丸ごと次ページへ送られて大きな空白を作るのではなく、今のページに残っている領域から自然に始まるようにする。

このリポジトリは upstream の `tcolorbox` 作者による公式配布物ではなく、upstream maintainer と提携しているものでもありません。

## 目次

- [まず使うなら](#まず使うなら)
- [見た目として何が変わるか](#見た目として何が変わるか)
- [どのファイルを使うのか](#どのファイルを使うのか)
- [手動コピーで試す方法](#手動コピーで試す方法)
- [プロジェクトごとに使う方法](#プロジェクトごとに使う方法)
- [個人用 TEXMF に入れる](#個人用-texmf-に入れる)
- [システム全体の TEXMF に入れる](#システム全体の-texmf-に入れる)
- [別パッケージの内部で `tcolorbox` が読み込まれる場合](#別パッケージの内部で-tcolorbox-が読み込まれる場合)
- [基本情報](#基本情報)
- [検証](#検証)
- [リポジトリ構成](#リポジトリ構成)
- [Upstream](#upstream)

## まず使うなら

文書では、`tcolorbox` の代わりにこのパッケージを読み込みます。

```tex
\usepackage[most]{breakble-tcolorbox}
```

読み込んだ後は、いつもの `tcolorbox` の書き方をそのまま使います。

```tex
\begin{tcolorbox}[breakable,title={Outer box}]
  Text before the nested box.

  \begin{tcolorbox}[breakable,title={Nested box}]
    Long nested content...
  \end{tcolorbox}
\end{tcolorbox}
```

同じ文書で次のように両方を書くことは避けてください。

```tex
\usepackage{tcolorbox}
\usepackage{breakble-tcolorbox}
```

`breakble-tcolorbox` はラッパーパッケージです。`most`, `skins`, `breakable` などのオプションを、このリポジトリに入っている改変済み `tcolorbox` に渡して読み込みます。

## 見た目として何が変わるか

元の `tcolorbox` では、通常の方法で入れ子にした `breakable` ボックスは、実質的にはその場でページ分割できません。そのため、内側のボックスが今のページの残り部分に収まらないと、内側のボックスが丸ごと次のページへ送られ、ページ下部に大きな空白ができることがあります。

`breakble-tcolorbox` では、内側のボックスを親の `breakable` ボックスのページ分割の流れに参加させます。そのため、内側のボックスの最初の断片が、今のページに残っている領域から始まります。

下の比較は、同じ A4 文書をコンパイルしたものです。左が元の `tcolorbox`、右が `breakble-tcolorbox` です。比較では、本文は同じまま、読み込むパッケージを切り替えています。

1ページ目では、元の `tcolorbox` がページ下部を大きく空けて内側のボックスを次ページへ送っている一方で、`breakble-tcolorbox` は同じページの残り領域から内側のボックスを始めています。2ページ目を見ると、右側の内側ボックスが実際にページをまたいで続いていることも確認できます。

![Nested breakable comparison page 1](docs/readme-demo/images/nested-breakable-comparison-page-000001.png)

![Nested breakable comparison page 2](docs/readme-demo/images/nested-breakable-comparison-page-000002.png)

同じ比較は PDF でも確認できます。

- `docs/readme-demo/nested-breakable-comparison.pdf`

サンプルの中心部分は、普通の `tcolorbox` の書き方です。

```tex
\begin{outerdemo}
Text before the nested box.

\begin{innerdemo}
Nested breakable content begins here.

% Long ordinary prose follows.
% 元の tcolorbox では、この内側ボックスが次ページへ送られます。
% breakble-tcolorbox では、ここから始まり、次ページへ続きます。
\end{innerdemo}

Text after the nested box.
\end{outerdemo}
```

このサンプルのソースは `docs/readme-demo/` に置いてあります。

- `nested-breakable-original.tex`: 元の `tcolorbox` を使う版
- `nested-breakable-breakble.tex`: `breakble-tcolorbox` を使う版
- `nested-breakable-body.tex`: 両者で共通の本文
- `nested-breakable-comparison.pdf`: 左に元の出力、右に `breakble-tcolorbox` の出力を並べた PDF

`breakble-tcolorbox` 版の冒頭は次のようになります。

```tex
\documentclass[a4paper,11pt]{article}
\usepackage[margin=24mm]{geometry}
\usepackage[most]{breakble-tcolorbox}

\input{nested-breakable-body.tex}
```

比較用の元版では、同じ本文に対して読み込み部分を次のようにしています。

```tex
\usepackage[most]{tcolorbox}
```

このリポジトリのルートからサンプル PDF を再生成する場合は、次のようにします。

```sh
cd docs/readme-demo
TEXINPUTS="$PWD:$PWD/../../vendor/tcolorbox-original//:" \
  latexmk -pdf -outdir=../../build/readme-demo/original nested-breakable-original.tex
TEXINPUTS="$PWD:$PWD/../../texmf/tex/latex//:" \
  latexmk -pdf -outdir=../../build/readme-demo/breakble nested-breakable-breakble.tex
```

## どのファイルを使うのか

文書から直接読み込む入口は、次のファイルです。

- `breakble-tcolorbox.sty`

コンパイル時には、同じ場所に次の実行時ファイルも必要です。これらはラッパーが自動で読むため、文書から手で読み込む必要はありません。

- `breakble-tcolorbox-runtime.sty`
- `breakble-tcb*.code.tex`

これらは upstream の `tcolorbox` 実行時ファイルを元にした改変済みコピーです。配布用ファイルには `breakble-` という接頭辞を付け、本家の `tcolorbox.sty` や `tcbbreakable.code.tex` と同じ名前にならないようにしています。

そのため、個人用 TEXMF やシステム TEXMF に入れても、`breakble-tcolorbox` を明示していない文書の

```tex
\usepackage{tcolorbox}
```

は通常どおり本家 `tcolorbox` を読みます。改変版を使うのは、次のように明示した文書だけです。

```tex
\usepackage[most]{breakble-tcolorbox}
```

このリポジトリには開発・検証用の `tcolorbox/` ディレクトリもあります。これは差分確認や検証スクリプトのための作業用コピーで、通常のインストール先ではありません。TEXMF に入れるときは、リポジトリ全体や `tcolorbox/` ではなく、次の配布用フォルダを使ってください。

```text
texmf/tex/latex/breakble-tcolorbox/
```

## 手動コピーで試す方法

TeX の探索パスを設定せずに試したい場合は、次のフォルダを使ってください。

- `drop-in/`

`drop-in/` の中には、コピー用の `breakble-tcolorbox/` フォルダが入っています。このフォルダを、コンパイルしたい `.tex` ファイルと同じ階層へコピーしてください。大量の `.sty` や `.code.tex` が文書フォルダ直下に散らばらないようにしています。

たとえば、次のような配置にします。

```text
your-document/
  main.tex
  breakble-tcolorbox/
    breakble-tcolorbox.sty
    breakble-tcolorbox-runtime.sty
    breakble-tcbbreakable.code.tex
    breakble-tcbskins.code.tex
    ...
```

この配置なら、文書側では次のように読み込みます。

```tex
\usepackage[most]{breakble-tcolorbox/breakble-tcolorbox}
```

この方法では、`TEXINPUTS` や `mktexlsr` は不要です。試用や、特定のプロジェクトで使いたい場合に向いています。

## プロジェクトごとに使う方法

ファイルを手動コピーせず、このリポジトリをそのまま置いて使いたい場合は、配布用 TEXMF ツリーを TeX の探索パスの先頭に置きます。

```sh
TEXINPUTS="/path/to/breakble-tcolorbox/texmf/tex/latex//:" latexmk -pdf main.tex
```

たとえば、文書の隣にこのリポジトリを置いているなら、次のようにできます。

```sh
TEXINPUTS="../breakble-tcolorbox/texmf/tex/latex//:" latexmk -pdf main.tex
```

末尾の `//` は重要です。TeX に「このディレクトリ以下を再帰的に探す」と伝えるためのものです。

TeX がどのファイルを見つけるかは、次のように確認できます。

```sh
TEXINPUTS="/path/to/breakble-tcolorbox/texmf/tex/latex//:" kpsewhich breakble-tcolorbox.sty
TEXINPUTS="/path/to/breakble-tcolorbox/texmf/tex/latex//:" kpsewhich tcolorbox.sty
```

`breakble-tcolorbox.sty` はこのリポジトリの `texmf/tex/latex/breakble-tcolorbox/` を指します。一方、`tcolorbox.sty` は通常どおり TeX Live / MacTeX / MiKTeX 側の本家 `tcolorbox` を指すのが期待される状態です。これにより、普通の `\usepackage{tcolorbox}` は本家のまま保てます。

## 個人用 TEXMF に入れる

毎回 `TEXINPUTS` を指定せずに使いたい場合は、個人用 TEXMF に入れるのが扱いやすいです。個人用 TEXMF は、TeX が自動で探しに行くユーザー専用の追加パッケージ置き場です。

この方法でやることは、次の 3 つです。

1. GitHub にあるこのリポジトリを、自分の PC に置く。
2. リポジトリ内の配布用フォルダだけを、個人用 TEXMF にコピーする。
3. TeX がそのファイルを見つけられるか確認する。

コマンドを打つだけで GitHub 上のファイルが直接 TeX に入るわけではありません。まず、このリポジトリを手元に用意して、その中にある次のフォルダをコピーします。

```text
texmf/tex/latex/breakble-tcolorbox/
```

このフォルダには `tcolorbox.sty` という名前のファイルを入れていません。そのため、通常の `\usepackage{tcolorbox}` は本家 `tcolorbox` を読み続け、`\usepackage{breakble-tcolorbox}` と書いた文書だけが改変版を使います。

### 1. GitHub から手元に持ってくる

`git` を使える場合は、好きな作業場所で次のようにします。

```sh
cd ~/Downloads
git clone https://github.com/artin-kagun/breakble-tcolorbox.git
cd breakble-tcolorbox
```

`git` を使わない場合は、GitHub のページで **Code** → **Download ZIP** を選び、ZIP を展開してください。その後、ターミナルや PowerShell で展開したフォルダへ移動します。

```sh
cd ~/Downloads/breakble-tcolorbox-main
```

以降のコマンドは、このリポジトリのルートで実行します。そこに `README.md` や `texmf/` が見えている状態です。

コピーするフォルダがあるか、先に確認しておくと安心です。

```sh
ls texmf/tex/latex/breakble-tcolorbox
```

少なくとも `breakble-tcolorbox.sty` や `breakble-tcolorbox-runtime.sty` が表示されれば、その場所で合っています。

### 2. 個人用 TEXMF の場所を確認する

macOS でも Windows でも、TeX Live / MacTeX を使っているなら次のコマンドが基本です。

```sh
kpsewhich -var-value=TEXMFHOME
```

よくある場所は次のとおりです。実際の場所は必ず上の `kpsewhich` で確認してください。

| 環境 | よくある `TEXMFHOME` |
| --- | --- |
| macOS / MacTeX | `~/Library/texmf` |
| Linux / TeX Live | `~/texmf` |
| Windows / TeX Live | `C:\Users\<ユーザー名>\texmf` |

### 3. macOS / Linux / TeX Live でコピーする

```sh
TEXMFHOME="$(kpsewhich -var-value=TEXMFHOME)"
mkdir -p "$TEXMFHOME/tex/latex"
rm -rf "$TEXMFHOME/tex/latex/breakble-tcolorbox"
cp -R texmf/tex/latex/breakble-tcolorbox "$TEXMFHOME/tex/latex/"
```

この 4 行は、順番に次のことをしています。

- `TEXMFHOME=...`: TeX が探しに行く個人用 TEXMF の場所を変数に入れる。
- `mkdir -p ...`: コピー先の `tex/latex` フォルダを作る。
- `rm -rf ...`: すでに古い `breakble-tcolorbox` が入っている場合だけ、そのフォルダを入れ直せるように消す。
- `cp -R ...`: GitHub から持ってきたリポジトリ内の `texmf/tex/latex/breakble-tcolorbox` を、個人用 TEXMF にコピーする。

消しているのは個人用 TEXMF 内の `breakble-tcolorbox` フォルダだけです。本家 `tcolorbox` や他の TeX パッケージは触りません。

### 4. Windows / TeX Live でコピーする

PowerShell では次のようにできます。

```powershell
$TEXMFHOME = kpsewhich -var-value=TEXMFHOME
New-Item -ItemType Directory -Force "$TEXMFHOME\tex\latex"

Remove-Item "$TEXMFHOME\tex\latex\breakble-tcolorbox" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item .\texmf\tex\latex\breakble-tcolorbox "$TEXMFHOME\tex\latex\" -Recurse -Force
```

これは、リポジトリ内の `texmf\tex\latex\breakble-tcolorbox` フォルダを、Windows の個人用 TEXMF の `tex\latex` の中へコピーしています。

### 5. Windows / MiKTeX

MiKTeX では、TeX Live と同じ `kpsewhich` 方式で分かる場合もありますが、MiKTeX Console でユーザー用の root directory を追加する方が分かりやすいことがあります。

1. 例として `C:\Users\<ユーザー名>\texmf` を作る。
2. その中に `tex\latex` を作る。
3. このリポジトリの `texmf\tex\latex\breakble-tcolorbox` フォルダを、作った `tex\latex` の中へコピーする。
4. MiKTeX Console でその `texmf` フォルダを root directory として追加する。
5. MiKTeX Console で file name database を更新する。

コマンドで行う場合は、環境によって次のような操作になります。

```powershell
initexmf --register-root=C:\Users\<ユーザー名>\texmf
initexmf --update-fndb
```

### 6. 確認する

`TEXMFHOME` では、TeX Live なら通常はファイル名データベースの更新なしで見つかります。もし TeX が見つけてくれない場合は、次を実行してください。

```sh
mktexlsr "$TEXMFHOME"
```

最後に確認します。

```sh
kpsewhich breakble-tcolorbox.sty
kpsewhich tcolorbox.sty
```

`kpsewhich breakble-tcolorbox.sty` は個人用 TEXMF 内の `breakble-tcolorbox` を指していれば成功です。`kpsewhich tcolorbox.sty` は通常どおり TeX Live / MacTeX / MiKTeX 側の本家 `tcolorbox` を指すのが期待される状態です。

つまり、個人用 TEXMF に入れても、普通の

```tex
\usepackage{tcolorbox}
```

は本家を読み、次のように書いた文書だけが改変版を使います。

```tex
\usepackage[most]{breakble-tcolorbox}
```

より詳しく調べたい場合は、次の語句で検索すると情報にたどり着きやすいです。

- `TeX Live TEXMFHOME`
- `MacTeX TEXMFHOME Library texmf`
- `Windows TeX Live TEXMFHOME kpsewhich`
- `MiKTeX local texmf root`
- `MiKTeX register root update fndb`
- `mktexlsr texhash 違い`

## システム全体の TEXMF に入れる

共有の TeX Live 環境に入れる場合は、`TEXMFLOCAL` を使います。

```sh
kpsewhich -var-value=TEXMFLOCAL
```

次の場所に、個人用 TEXMF と同じく安全な配布用フォルダを置きます。

```text
<TEXMFLOCAL>/tex/latex/breakble-tcolorbox/
```

例:

```sh
TEXMFLOCAL="$(kpsewhich -var-value=TEXMFLOCAL)"
sudo mkdir -p "$TEXMFLOCAL/tex/latex"
sudo cp -R texmf/tex/latex/breakble-tcolorbox "$TEXMFLOCAL/tex/latex/"
sudo mktexlsr
```

システム全体に入れる場合も、通常の `\usepackage{tcolorbox}` は本家 `tcolorbox` を読み続ける設計です。ただし、共有環境では他の利用者にも `breakble-tcolorbox` が見えるようになるため、管理者が意図している場合に選んでください。

## 別パッケージの内部で `tcolorbox` が読み込まれる場合

別パッケージや文書クラスが内部で `\RequirePackage{tcolorbox}` を実行することがあります。この場合は、読み込み順によって結果が変わります。

### `breakble-tcolorbox` を先に読める場合

自分でプリアンブルの順番を調整できるなら、`tcolorbox` を内部で使うパッケージより先に `breakble-tcolorbox` を読み込んでください。

```tex
\usepackage[most]{breakble-tcolorbox}
\usepackage{some-package-that-uses-tcolorbox}
```

この場合、後から別パッケージが `\RequirePackage{tcolorbox}` を実行しても、LaTeX から見ると `tcolorbox` はすでに読み込み済みです。そのため、別パッケージも `breakble-tcolorbox` が読み込んだ改変済み実行時ファイルを共有します。

これは、個人用 TEXMF、システム TEXMF、プロジェクトごとの `TEXINPUTS`、`drop-in/` のどの方法で入れていても同じです。`drop-in/` 方式では、読み込み行だけ次のようになります。

```tex
\usepackage[most]{breakble-tcolorbox/breakble-tcolorbox}
\usepackage{some-package-that-uses-tcolorbox}
```

この使い方なら、TeX 環境全体の本家 `tcolorbox` を置き換えずに、その文書だけで改変版を使えます。

### 先に本家 `tcolorbox` が読み込まれてしまう場合

文書クラスや別パッケージが、`breakble-tcolorbox` より前に本家 `tcolorbox` を読み込んでしまう場合は、あとから差し替えることはできません。一度読み込まれた LaTeX パッケージを、別の実装に静かに入れ替えると、実行時ファイルが混ざって壊れる可能性があるためです。

この場合、`breakble-tcolorbox` はそのまま続行せず、読み込み順の問題として止まるようにしています。基本的な対処は、`breakble-tcolorbox` を先に読むようにプリアンブルや文書クラスの設定を変えることです。

### 読み込み順を変えられない場合の最終手段

どうしても読み込み順を変えられず、その文書だけで改変版を強制したい場合は、開発用の `tcolorbox/` を本家より先に TeX の探索パスへ置く方法があります。

これは通常の `\usepackage{tcolorbox}` も改変版へ向ける、意図的な上書きです。個人用 TEXMF やシステム TEXMF に入れる通常の方法としては使わないでください。使う場合も、対象の文書をコンパイルするときだけに限定してください。

```sh
TEXINPUTS="/path/to/breakble-tcolorbox/tcolorbox//:" latexmk -pdf main.tex
```

この上書き方式を使うときは、`.log` ファイルや `kpsewhich` で、どの `tcolorbox.sty` が読まれているか必ず確認してください。意図せず通常の文書まで改変版へ向いていないかを見るためです。

### オプション衝突を避ける

```tex
\usepackage[most]{breakble-tcolorbox}
```

後から読み込まれるパッケージが `tcolorbox` にオプションを渡す場合、すでに読み込まれた `tcolorbox` へ別のオプションを追加しようとして `Option clash` エラーになることがあります。

必要になりそうなライブラリは、最初の `breakble-tcolorbox` 読み込み時にまとめて指定してください。`most` はよく使われる `tcolorbox` ライブラリをまとめて読み込むため、多くの場合はこれで足ります。

## 基本情報

- ベース: `tcolorbox` 6.10.0, tag `v6.10.0`
- このコピーに使った upstream commit: `057ff62f77aeef399251ac4fca98d1a20c36ab32`
- ライセンス: upstream `tcolorbox` と同じく LPPL 1.3c or later
- メンテナンス: 非公式版です。upstream の `tcolorbox` 作者による保守物ではありません。

## 検証

開発中に固めた入れ子 `breakable` の要件は `docs/nested-breakable-requirements.md` に残しています。

upstream の単体サンプルとマニュアルソースを、それぞれ次の 2 通りでコンパイルします。

- 元の `tcolorbox` 6.10.0
- この `breakble-tcolorbox` 配布版

生成されたページをピクセル単位で比較し、左に元の出力、右に `breakble-tcolorbox` 版を並べた比較 PDF も生成します。

### PDF で確認できるもの

具体的な出力を見たい場合は、まず次の PDF を見てください。これらはリポジトリに含めてあります。

- `docs/readme-demo/nested-breakable-comparison.pdf`:
  README の説明に使っている基本の比較例です。左が元の `tcolorbox`、右が `breakble-tcolorbox` です。
- `verification/nested-behavior/pdf/a4-nested-behavior-side-by-side.pdf`:
  入れ子の `breakable` ボックスが、元の `tcolorbox` と `breakble-tcolorbox` でどう違うかをケースごとに並べた比較 PDF です。
- `verification/nested-behavior/pdf/a4-nested-title-mix.pdf`:
  継続タイトルあり・なしが混ざる入れ子で、上下の余白や重なりが自然になるかを確認する PDF です。
- `verification/nested-behavior/pdf/a4-nested-title-mix-deep.pdf`:
  より深い入れ子で、継続タイトルあり・なしが混ざる場合を確認する PDF です。
- `verification/nested-behavior/pdf/a4-nested-breakable-stress.pdf`:
  途中ページから始まるボックス、タイトルなしの継続、多重入れ子、装飾付きの上下部分などをまとめて確認する PDF です。
- `verification/nested-behavior/pdf/a4-nested-display-math-overlap.pdf`:
  入れ子の `breakable` ボックス内に display math がある場合に、数式直後の本文が数式領域へ重ならず、普通の行間で続くことを確認する PDF です。
- `verification/nested-behavior/pdf/a4-nested-display-math-overlap-xelatex.pdf`:
  同じ display math サンプルを XeLaTeX でコンパイルした PDF です。
- `verification/nested-behavior/pdf/a4-proof-nested-overlap-uplatex.pdf`:
  日本語の証明文に display math を含めた入れ子 `breakable` を upLaTeX で確認する PDF です。
- `verification/nested-behavior/pdf/a4-nested-mixed-continuous.pdf`:
  タイトルあり・タイトルなしが混ざる多段ネストを、普通の本文が続く形で確認する PDF です。
- `verification/nested-behavior/pdf/a4-titleless-nesting-depths.pdf`:
  タイトルなしの入れ子を 2, 3, 4, 5, 6 段で確認する PDF です。
- `verification/nested-behavior/pdf/a4-titleless-reach-reference.pdf`:
  入れ子なしの通常の `tcolorbox` がページ下部へどこまで到達するかを見るための基準 PDF です。
- `verification/nested-behavior/pdf/b5-nested-breakable-smoke.pdf`:
  A4 以外の紙面でも、紙面サイズを固定した実装になっていないことを確認するための B5 サンプルです。

upstream の単体サンプルについては、左に元の出力、右に `breakble-tcolorbox` 版を並べた比較 PDF があります。

- `verification/example-parity/side-by-side/tcolorbox-example/tcolorbox-example__original-side-by-side.pdf`
- `verification/example-parity/side-by-side/tcolorbox-example-poster/tcolorbox-example-poster__original-side-by-side.pdf`
- `verification/example-parity/side-by-side/tcolorbox-tutorial-poster/tcolorbox-tutorial-poster__original-side-by-side.pdf`

### マニュアル全体で確認する場合

upstream のマニュアル本文は、次のファイルです。

- `docs/tcolorbox/tcolorbox.tex`

このファイルから、`docs/tcolorbox/tcolorbox.doc.*.tex` の各断片が読み込まれます。`breakble-tcolorbox` でマニュアル全体をコンパイルして確認する場合は、次を実行します。

```sh
scripts/check-upstream-manual-parity.py
```

このスクリプトは検証用に、開発用の `tcolorbox/` を一時的に TeX の探索パス先頭へ置きます。upstream のマニュアルソースは通常の `\usepackage{tcolorbox}` を含むため、その呼び出しを改変版へ向けて比較するためです。これは通常のインストール方法ではなく、検証スクリプト内だけの扱いです。

実行後、主な出力は次の場所にできます。

- `breakble-tcolorbox` でコンパイルしたマニュアル:
  `verification/manual-parity/sources/breakble/tcolorbox.pdf`
- 元の `tcolorbox` でコンパイルしたマニュアル:
  `verification/manual-parity/sources/original/tcolorbox.pdf`
- 左に元の出力、右に `breakble-tcolorbox` 版を並べたマニュアル比較 PDF:
  `verification/manual-parity/side-by-side/tcolorbox-manual/tcolorbox-side-by-side.pdf`
- 実行結果のレポート:
  `verification/manual-parity/report.md`

`verification/manual-parity/` は、マニュアル全体の PDF やレンダリング画像を含む生成物なので、Git では無視しています。手元で上のスクリプトを実行すると再生成されます。

入れ子挙動のレポート:

- `verification/nested-behavior/report.md`

単体サンプルの一致確認レポート:

- `verification/example-parity/report.md`

現在の検証結果では、upstream example は 3/3 件でページ数一致・pixel 一致、upstream manual は 568/568 ページで pixel 一致しています。入れ子挙動のサンプルは pdfLaTeX / XeLaTeX / upLaTeX の代表ビルドを確認しています。LuaLaTeX については、この作業環境では `luaotfload` が文書処理前に `no writeable cache path` で停止したため、PDF 生成までは確認できていません。

単体サンプルの一致確認を再生成:

```sh
scripts/check-upstream-example-parity.py
```

マニュアル一致確認の再生成:

```sh
scripts/check-upstream-manual-parity.py
```

公開用の検証スクリプトをまとめて実行:

```sh
scripts/run-full-verification.sh
```

これらのスクリプトは `latexmk`, `pdflatex`, `biber`, `makeindex`, `pdfinfo`, `pdftopng` を必要とします。`pygmentize` が `PATH` 上にない場合は、その実行中に使う Pygments を `/tmp` にインストールします。

## リポジトリ構成

- `breakble-tcolorbox.sty`: 文書から読み込む公開用ラッパーパッケージ
- `breakble-tcolorbox-runtime.sty`, `breakble-tcb*.code.tex`: 本家と同名にならないようにした改変済み実行時ファイル
- `texmf/tex/latex/breakble-tcolorbox/`: 個人用 TEXMF やシステム TEXMF へコピーする配布用フォルダ
- `tcolorbox/`: 開発・検証用の改変済み upstream 実行時ファイル
- `vendor/tcolorbox-original/`: 出力一致検証に使う未改変 upstream 実行時ファイル
- `docs/nested-breakable-requirements.md`: 入れ子 `breakable` 挙動について開発中に固めた要件
- `docs/tcolorbox/`: 出力一致検証に使う upstream のドキュメント、単体サンプルソース、画像など
- `docs/readme-demo/`: README の比較画像に使う A4 サンプル
- `docs/samples/`: タイトルなし入れ子などの追加サンプル
- `drop-in/`: `.tex` と同じ階層へフォルダごとコピーして使うためのファイル一式
- `scripts/build-safe-runtime-tree.py`: `tcolorbox/` から同名衝突を避ける配布用実行時ファイルを生成するスクリプト
- `verification/example-parity/`: 生成済みの一致確認レポート、ソースコピー、左右比較 PDF
- `verification/nested-behavior/`: 入れ子 `breakable` の確認用レポートと PDF
- `verification/manual-parity/`: 生成されるマニュアル一致確認レポート、ソースコピー、レンダリング画像、左右比較 PDF

## Upstream

このパッケージは Thomas F. Sturm 氏の `tcolorbox` を元にしています。

Upstream project:
<https://github.com/T-F-S/tcolorbox>

このリポジトリは upstream maintainer と提携しておらず、upstream maintainer による承認を受けたものでもありません。
