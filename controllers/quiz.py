import openai

openai.api_key = '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'

def generate_quiz(theme):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたは助けになるアシスタントです。"},
            {"role": "user", "content": f"{theme}についての一問一答のような簡単なクイズを一つだけ作成してください。回答はかならず、 '問題: ... 答え: ...'という形式で出力してください"},
        ],
        max_tokens=70
    )

    print('checkpoint5')
    assistant_reply = response['choices'][0]['message']['content']

    if "答え:" in assistant_reply:
        print('checkpoint6')
        question, answer = assistant_reply.split("答え:", 1)
        question = question.replace("問題:", "").strip()
        return question, answer.strip()
    else:
        return "予期しない形式の応答が返されました", ""
