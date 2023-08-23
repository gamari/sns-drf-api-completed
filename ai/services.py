import openai
from decouple import config

openai.api_key = config("OPEN_AI_KEY")

# TODO 動かない
def generate_tweets(num_tweets=3):
    tweets = []

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "user",
            "content": f"{num_tweets}個のツイートを作成してください。ただし、ツイート間には「---」を入れて仕切りをつけてください。連番はつけないでください。emotionは使ってはいけません。"
            }
        ],
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        max_tokens=280*num_tweets,
    )

    generated_content = response.choices[0].message.content.strip().split("---")
    print(generate_tweets)
    for tweet in generated_content:
        if tweet:
            tweets.append(tweet)

    return tweets[:num_tweets]