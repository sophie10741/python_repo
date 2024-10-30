import requests
import tkinter as tk
from tkinter import messagebox

class YandexGPT:
    def __init__(self, token, catalog):
        self.token = token
        self.catalog = catalog

    def send_request(self, question):
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        prompt = {
            "modelUri": f'gpt://{self.catalog}/yandexgpt-lite',
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 200
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Отвечай цитатами из книг"
                },
                {
                    "role": "user",
                    "text": question
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.token}"
        }

        response = requests.post(url, headers=headers, json=prompt)
        text = response.json().get('result', {}).get('alternatives', [{}])[0].get('message', {}).get('text', "Ошибка при получении ответа")
        return text

#  графический интерфейс с Tkinter
def create_gui():
    def get_answer():
        question = question_entry.get()
        if question:
            try:
                result = bot.send_request(question)
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, result)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось получить ответ: {e}")
        else:
            messagebox.showwarning("Предупреждение", "Введите вопрос.")

    token = ""
    catalog = ""
    bot = YandexGPT(token, catalog)

    root = tk.Tk()
    root.title("YandexGPT Chat")

    tk.Label(root, text="Введите вопрос:").pack(pady=5)
    question_entry = tk.Entry(root, width=50)
    question_entry.pack(pady=5)

    tk.Button(root, text="Получить ответ", command=get_answer).pack(pady=5)

    result_text = tk.Text(root, height=10, width=50)
    result_text.pack(pady=5)

    root.mainloop()

create_gui()
