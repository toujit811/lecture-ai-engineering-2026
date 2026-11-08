# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：askは一般的な回答をしてくるが、agentはこのコースにおける意味を回答してくれる。
- `--trace` で見えたツール呼び出し（ツール名と引数）：
  - [tool call]   search_glossary({'query': 'LoRA'})
  - [tool call]   search_glossary({'query': 'QLoRA'})
  - [tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
  - [tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
  - [usage] RunUsage(cost=Decimal('0.0008338'), details={'text_prompt_tokens': 1196}, input_text_tokens=1196, input_tokens=1196, output_tokens=190, requests=2, tool_calls=2)
- 1つの質問での LLM 呼び出し回数（`requests`）：2回
- 追加したツールと、docstring に書いた説明：
```python
def make_quiz(lecture: int) -> str:
    """
    指定した回の用語から 1つを選び、確認問題と答えを返す。
    「第2回の確認問題を出して」のように、
    復習用の問題を求められたときに使う。
    """
    # 1. load_glossary() から lecture が一致する用語を集める
    # # 2. 1 つ選ぶ（random.choice）
    # # 3. 問題と答えを文字列で返す（ json.dumps など）
```

## 宿題

- 取り組んだレベル：基礎
- やったこと：
  1. 「- 用語や講座に固有のことを答える前に、必ず search_glossary で用語集を確認する。」を削除して実行した。
  1. 「1つだけ入れる→まとめて入れる」に変更して実行した。
- 結果：
  1. search_glossaryは呼ばれたが、回答が少し異なっていた。リクエスト回数、ツールを呼ぶ回数、引数の渡し方は変わらなかった。

  1. リクエスト回数は変わらなかった。しかし、ツールを呼ぶ回数と引数の渡し方は変わった。引数は、「LoRA QLoRA」を１回で渡していた。
- 気づき・疑問：
  コードは一切変更してないのに、コメントのようなものを変更したら、処理が変わった。
