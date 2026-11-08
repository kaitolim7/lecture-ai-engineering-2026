# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：ほぼ同じを確認
- `--list-tools` で確認したツール：`search_glossary(query)`, `get_lecture_summary(lecture)`, `make_quiz(lecture)`
- `--trace` で見えたツール呼び出し（ツール名と引数）：`make_quiz(lecture=2)`。用語「過学習」の意味を問題として出題し、答えを表示せずに利用者の回答を促した
- 1つの質問での LLM 呼び出し回数（`requests`）：2回（ツール呼び出し1回）
- 追加したツールと、docstring に書いた説明：`make_quiz(lecture: int)`。指定した回の用語から確認問題を1問作り、問題と答えを返す。確認問題を求められたときに使うことを説明した
- テスト：`uv run pytest -q` を実行し、17件すべて成功

## 宿題

- 取り組んだレベル：基礎
- やったこと：`app/tools.py` の `search_glossary` の docstring だけを変更し、「用語を1つだけ」から「関連する用語をまとめて」検索するよう説明した。同じ質問「LoRAとQLoRAの違いは？」を変更前後で `--trace` 付きで実行した
- 結果：変更前は `search_glossary(query='LoRA')` と `search_glossary(query='QLoRA')` の2回、変更後は `search_glossary(query='LoRA QLoRA')` の1回になった。変更後も用語集から両方の定義を取得し、回答した。LLM 呼び出し回数は変更前後とも2回、ツール呼び出し回数は2回から1回に減った
- 気づき・疑問：ツールの docstring はモデルがツールをどう使うかに影響する。関連語をまとめて検索するとツール呼び出しは減ったが、LLM 呼び出し回数は変わらなかった
