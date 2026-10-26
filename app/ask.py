"""第1回: 素のLLMと会話するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

最初の質問の後は、質問を入力して続けて会話できる。Ctrl+C または Ctrl+D で終了する。

ツールは持たない「素の」呼び出し。Chat API が会話履歴を保持する。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time

import readline

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"

readline.parse_and_bind("set editing-mode emacs")
readline.parse_and_bind("set enable-bracketed-paste on")


def ask(chat, question: str) -> str:
    started_at = time.perf_counter()
    response = chat.send_message(question)
    elapsed_seconds = time.perf_counter() - started_at

    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count
    output_tokens = usage.candidates_token_count
    print(f"[応答時間] {elapsed_seconds:.2f}秒")
    print(f"[トークン数] 入力: {input_tokens} / 出力: {output_tokens} / 合計: {input_tokens + output_tokens}")

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        client = genai.Client(api_key=get_api_key())
        chat = client.chats.create(model=MODEL)
        question = args.question or DEFAULT_QUESTION
        readline.add_history(question)
        while True:
            print(f"\n[質問] {question}")
            print(ask(chat, question))
            question = input("\n次の質問（終了: Ctrl+C）> ")
            if question:
                readline.add_history(question)
    except (EOFError, KeyboardInterrupt):
        print("\n終了しました。")
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
