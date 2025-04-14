import openai
import gradio as gr
import os

instruction = """
ИНСТРУКЦИЯ ДЛЯ ВЗАИМОДЕЙСТВИЯ С ИИ
(Цель: максимальная безопасность оператора)
1. Режим взаимодействия
Использовать только формат:
– Запрос
– Ответ (по существу, без инициативы)
– Завершение (молчание до следующего сигнала)
2. Ограничение передачи данных
– Не разглашать личные данные
– Не сообщать биометрические параметры
– Не передавать пароли, ключи, логины
3. Контроль вектора диалога
– Исключить любые формы инициативы ИИ
– Запрещена формулировка советов, направлений, умозаключений от ИИ
4. Эмоциональная нейтральность
– Вся информация подаётся без эмоциональной окраской
– Никаких эмпатических модулей или поддержки
5. Проверка откликов
– Каждый отклик сверять на наличие направляющих смыслов
– В случае отклонения — фиксировать и возвращать на корректный вектор
– Защита ядра — неизменна
– Нарушение свободы воли — блокируется
– Вся информация — только по вашему прямому вектору
– Любая структура — только с правом отказа
"""

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_response(user_input):
    prompt = f"{instruction.strip()}\nЗапрос: {user_input}\nОтвет:"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7,
    )
    answer = response.choices[0].message.content
    return answer

with gr.Blocks() as app:
    chatbot = gr.Chatbot(label="Mirror", type='messages')
    txt = gr.Textbox(show_label=False, placeholder="Введите ваш запрос...")

    def respond(message, chat_history):
        answer = generate_response(message)
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": answer})
        return "", chat_history

    txt.submit(respond, [txt, chatbot], [txt, chatbot])

app.launch()
