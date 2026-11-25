import csv
import time
from openai import OpenAI

client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama', timeout=180, max_retries=0)
prompts = [
    'Поясни різницю між GET і POST у PHP.',
    'Напиши функцію PHP для перевірки email.',
    'Поясни, що таке SQL Injection та як від неї захиститися.',
    'Напиши SQL-запит для вибірки користувачів старше 18 років із таблиці users з полем age.',
    'Поясни різницю між include та require у PHP.',
    'Напиши функцію JavaScript для перевірки парного числа.',
    'Поясни принцип MVC.',
    'Поясни різницю між cookies та sessions.',
    'Як створити нову гілку в Git?',
    'Знайди синтаксичну помилку в PHP-коді: echo $name',
]
with open('quality_results.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['model', 'number', 'prompt', 'answer', 'seconds', 'error'])
    for model in ['qwen3:4b', 'qwen3:1.7b']:
        for i, prompt in enumerate(prompts, 1):
            print(f'{model}: {i}/10', flush=True)
            start = time.monotonic()
            answer, error = '', ''
            try:
                result = client.chat.completions.create(model=model, messages=[{'role':'system','content':'Ти помічник програміста. Відповідай українською, стисло, точно, з прикладом за потреби.'},{'role':'user','content':prompt}], temperature=0, seed=1, max_tokens=350, reasoning_effort='none')
                answer = result.choices[0].message.content or ''
                if not answer.strip():
                    error = 'Empty response'
            except Exception as exc:
                error = str(exc)
                print(error, flush=True)
            writer.writerow([model, i, prompt, answer, round(time.monotonic()-start, 3), error])
            f.flush()
print('Saved: quality_results.csv')
