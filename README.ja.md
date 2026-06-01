# breakble-tcolorbox

[English](README.md) | [日本語](README.ja.md)

`breakble-tcolorbox` は
[`tcolorbox`](https://github.com/T-F-S/tcolorbox) 6.10.0 を元にした、非公式の改変版です。

公開されている `tcolorbox` の使い方はそのままに、ひとつの挙動だけを狭く変更しています。親の `tcolorbox` が `breakable` のとき、その中に入れた通常の `breakable` な `tcolorbox` も、親のページ分割の流れに合わせて分割できるようにします。

目指している状態は次のとおりです。

- 入れ子ではない普通の `tcolorbox` の出力は、元の `tcolorbox` と同じになる。
- upstream の example や manual source の出力は、元の `tcolorbox` と同じになる。
- `breakable` な box の中に長い `breakable` box を入れたとき、内側の box が丸ごと次ページへ送られて大きな空白を作るのではなく、今のページに残っている領域から自然に始まる。

このリポジトリは upstream の `tcolorbox` 作者による公式配布物ではなく、upstream maintainer と提携しているものでもありません。

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

`breakble-tcolorbox` は wrapper です。`most`, `skins`, `breakable` などのオプションを、このリポジトリに入っている改変済み `tcolorbox` に渡して読み込みます。

## 見た目として何が変わるか

元の `tcolorbox` では、通常の入れ子になった `breakable` box は、実質的にはそこでページ分割できません。そのため、内側の box が今のページの残り部分に収まらないと、内側の box が丸ごと次のページへ送られ、ページ下部に大きな空白ができることがあります。

`breakble-tcolorbox` では、内側の box を親の `breakable` box に管理される断片として分割します。そのため、内側の box の最初の断片が、今のページに残っている領域から始まります。

下の比較は、同じ A4 文書をコンパイルしたものです。左が元の `tcolorbox`、右が `breakble-tcolorbox` です。意味のある違いは、読み込むパッケージだけです。

1ページ目では、元の `tcolorbox` がページ下部を大きく空けて内側の box を次ページへ送っている一方で、`breakble-tcolorbox` は同じページの残り領域から内側の box を始めています。2ページ目を見ると、右側の内側 box が実際にページをまたいで続いていることが分かります。

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
% 元の tcolorbox では、この内側 box が次ページへ送られます。
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

`breakble-tcolorbox` 版の冒頭は次のようになっています。

```tex
\documentclass[a4paper,11pt]{article}
\usepackage[margin=24mm]{geometry}
\usepackage[most]{breakble-tcolorbox}

\input{nested-breakable-body.tex}
```

比較用の元版では、同じ本文に対して読み込み部分だけを次のようにしています。

```tex
\usepackage[most]{tcolorbox}
```

このリポジトリのルートから、サンプルPDFを再生成する場合は次のようにします。

```sh
cd docs/readme-demo
TEXINPUTS="$PWD:$PWD/../../vendor/tcolorbox-original//:" \
  latexmk -pdf -outdir=../../build/readme-demo/original nested-breakable-original.tex
TEXINPUTS="$PWD:$PWD/../..:$PWD/../../tcolorbox//:" \
  latexmk -pdf -outdir=../../build/readme-demo/breakble nested-breakable-breakble.tex
```

## どのファイルを使うのか

ユーザーが文書から直接読み込む入口は、次のファイルです。

- `breakble-tcolorbox.sty`

ただし、コンパイル時には次のディレクトリも必要です。

- `tcolorbox/`

この `tcolorbox/` ディレクトリは、upstream の runtime files を改変したコピーです。中には `tcolorbox.sty`、`tcbbreakable.code.tex` や `tcbskins.code.tex` などの library files、一部の skin が使う画像ファイルが入っています。

`tcolorbox/` は、ユーザーが文書内で直接読み込むものではありません。また、一部のファイルだけを抜き出してコピーするのも避けてください。`breakble-tcolorbox.sty` と `tcolorbox/` ディレクトリをセットで使う、という理解で大丈夫です。

文書内で書くのはこれだけです。

```tex
\usepackage[most]{breakble-tcolorbox}
```

## プロジェクトごとに使う方法

まず試すなら、この方法が一番安全です。特定の文書をコンパイルするときだけ、このリポジトリを TeX の探索パスの先頭に置きます。

```sh
TEXINPUTS="/path/to/breakble-tcolorbox//:" latexmk -pdf main.tex
```

たとえば、文書の隣にこのリポジトリを置いているなら、次のようにできます。

```sh
TEXINPUTS="../breakble-tcolorbox//:" latexmk -pdf main.tex
```

末尾の `//` は重要です。TeX に「このディレクトリ以下を再帰的に探す」と伝えるためのもので、これがないと `tcolorbox/` の中にある runtime files が見つからないことがあります。

TeX がどのファイルを見つけるかは、次のように確認できます。

```sh
TEXINPUTS="/path/to/breakble-tcolorbox//:" kpsewhich breakble-tcolorbox.sty
TEXINPUTS="/path/to/breakble-tcolorbox//:" kpsewhich tcolorbox.sty
```

どちらも、このリポジトリ内のパスを指していればOKです。

## 個人用 TEXMF に入れる方法

毎回 `TEXINPUTS` を指定せずに使いたい場合は、個人用の TEXMF tree に入れます。

まず、個人用 TEXMF の場所を確認します。

```sh
kpsewhich -var-value=TEXMFHOME
```

MacTeX では、よく次の場所になります。

```text
~/Library/texmf
```

次のようにディレクトリを作り、必要なものをコピーします。

```sh
TEXMFHOME="$(kpsewhich -var-value=TEXMFHOME)"
mkdir -p "$TEXMFHOME/tex/latex/breakble-tcolorbox"

cp breakble-tcolorbox.sty "$TEXMFHOME/tex/latex/breakble-tcolorbox/"
cp -R tcolorbox "$TEXMFHOME/tex/latex/breakble-tcolorbox/"
```

`TEXMFHOME` では、通常はファイル名データベースの更新なしで見つかります。もし TeX が見つけてくれない場合は、次を実行してください。

```sh
mktexlsr "$TEXMFHOME"
```

最後に確認します。

```sh
kpsewhich breakble-tcolorbox.sty
kpsewhich tcolorbox.sty
```

この方法で入れた場合、`kpsewhich tcolorbox.sty` も `breakble-tcolorbox/tcolorbox/` 以下の改変済みファイルを指すのが期待される状態です。このパッケージは、wrapper から改変済みの `tcolorbox.sty` を読み込む形で動くためです。

## システム全体の TEXMF に入れる方法

共有の TeX Live 環境に入れる場合は、`TEXMFLOCAL` を使います。

```sh
kpsewhich -var-value=TEXMFLOCAL
```

次の場所に、同じく `breakble-tcolorbox.sty` と `tcolorbox/` を置きます。

```text
<TEXMFLOCAL>/tex/latex/breakble-tcolorbox/
```

例:

```sh
TEXMFLOCAL="$(kpsewhich -var-value=TEXMFLOCAL)"
sudo mkdir -p "$TEXMFLOCAL/tex/latex/breakble-tcolorbox"
sudo cp breakble-tcolorbox.sty "$TEXMFLOCAL/tex/latex/breakble-tcolorbox/"
sudo cp -R tcolorbox "$TEXMFLOCAL/tex/latex/breakble-tcolorbox/"
sudo mktexlsr
```

ただし、この方法では、その TeX 環境でコンパイルする文書に対して、改変済み `tcolorbox` が本家より先に見つかる可能性があります。影響範囲が広いので、必要性がはっきりしている場合だけにしてください。

## 別パッケージの内部で `tcolorbox` が読み込まれる場合

ここは少し注意が必要です。

自分で preamble の順番を調整できるなら、`tcolorbox` を内部で使うパッケージより前に `breakble-tcolorbox` を読み込んでください。

```tex
\usepackage[most]{breakble-tcolorbox}
\usepackage{some-package-that-uses-tcolorbox}
```

この場合、後からそのパッケージが `\RequirePackage{tcolorbox}` を実行しても、LaTeX から見ると `tcolorbox` はすでに読み込み済みです。つまり、`breakble-tcolorbox` が読み込んだ改変済み `tcolorbox` が使われます。

一方で、document class やパッケージが preamble より前、または `breakble-tcolorbox` より前に `tcolorbox` を読み込んでしまう場合、あとから wrapper で差し替えることはできません。その場合は、このリポジトリの `tcolorbox/` を本家 `tcolorbox` より先に TeX の探索パスへ置き、wrapper は後から読み込まないでください。

```sh
TEXINPUTS="/path/to/breakble-tcolorbox/tcolorbox//:" latexmk -pdf main.tex
```

これにより、内部の `\RequirePackage{tcolorbox}` が、改変済み runtime copy を直接見つけます。次のコマンドや `.log` ファイルで、どの `tcolorbox.sty` が読まれているか確認してください。

```sh
TEXINPUTS="/path/to/breakble-tcolorbox/tcolorbox//:" kpsewhich tcolorbox.sty
```

また、後から読み込まれるパッケージが `tcolorbox` にオプションを渡す場合は、できるだけ先に広めのオプションを読み込んでおくと option clash を避けやすくなります。

```tex
\usepackage[most]{breakble-tcolorbox}
```

`most` は通常使われる `tcolorbox` libraries をまとめて読み込むため、多くの場合はこれで足ります。

## 状態

- ベース: `tcolorbox` 6.10.0, tag `v6.10.0`
- このコピーに使った upstream commit: `057ff62f77aeef399251ac4fca98d1a20c36ab32`
- ライセンス: upstream `tcolorbox` と同じく LPPL 1.3c or later
- メンテナンス: 非公式版です。upstream の `tcolorbox` 作者による保守物ではありません。

## 検証

開発中に固めた nested breakable の要件は `docs/nested-breakable-requirements.md` に残しています。

upstream の standalone example と upstream manual source を、それぞれ次の 2 通りでコンパイルします。

- original `tcolorbox` 6.10.0
- この `breakble-tcolorbox` 配布版

生成されたページを pixel 単位で比較し、左に original、右に breakble を並べた side-by-side PDF も生成します。

standalone example のレポート:

- `verification/example-parity/report.md`
- `verification/example-parity/side-by-side/tcolorbox-example/tcolorbox-example__original-side-by-side.pdf`
- `verification/example-parity/side-by-side/tcolorbox-example-poster/tcolorbox-example-poster__original-side-by-side.pdf`
- `verification/example-parity/side-by-side/tcolorbox-tutorial-poster/tcolorbox-tutorial-poster__original-side-by-side.pdf`

nested behavior の確認資料:

- `verification/nested-behavior/report.md`
- `verification/nested-behavior/pdf/a4-nested-behavior-side-by-side.pdf`
- `verification/nested-behavior/pdf/a4-nested-title-mix.pdf`
- `verification/nested-behavior/pdf/a4-nested-title-mix-deep.pdf`
- `verification/nested-behavior/pdf/a4-nested-breakable-stress.pdf`

manual parity の出力は、manual parity script によって `verification/manual-parity/` 以下に生成されます。この検証では `docs/tcolorbox/tcolorbox.tex` をコンパイルし、そこから読み込まれる `tcolorbox.doc.*.tex` 断片を含めて、全ページを比較します。

standalone example parity の再生成:

```sh
scripts/check-upstream-example-parity.py
```

manual parity の再生成:

```sh
scripts/check-upstream-manual-parity.py
```

公開用の検証スクリプトをまとめて実行:

```sh
scripts/run-full-verification.sh
```

これらのスクリプトは `latexmk`, `pdflatex`, `biber`, `makeindex`, `pdfinfo`, `pdftopng` を必要とします。`pygmentize` が `PATH` 上にない場合は、その実行中だけ使う Pygments を `/tmp` にインストールします。

## リポジトリ構成

- `breakble-tcolorbox.sty`: 文書から読み込む公開用 wrapper package
- `tcolorbox/`: wrapper が読み込む改変済み runtime package files
- `vendor/tcolorbox-original/`: parity check 用の未改変 upstream runtime files
- `docs/nested-breakable-requirements.md`: nested breakable 挙動について開発中に固めた要件
- `docs/tcolorbox/`: parity check に使う upstream documentation、standalone example sources、assets
- `docs/readme-demo/`: README の比較画像に使う小さな A4 サンプル
- `verification/example-parity/`: 生成済み parity report、source copies、side-by-side PDFs
- `verification/nested-behavior/`: nested breakable の確認用レポートとPDF
- `verification/manual-parity/`: 生成される manual parity report、source copies、rendered pages、side-by-side PDF

## Upstream

このパッケージは Thomas F. Sturm 氏の `tcolorbox` を元にしています。

Upstream project:
<https://github.com/T-F-S/tcolorbox>

このリポジトリは upstream maintainer と提携しておらず、upstream maintainer による承認を受けたものでもありません。
