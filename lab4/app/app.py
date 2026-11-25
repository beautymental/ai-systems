import json
import urllib.request
import urllib.error
import tkinter as tk
from tkinter import ttk
import threading

def ask():
    prompt = entry.get("1.0", "end").strip()
    if not prompt:
        status.set("Введіть запит.")
        return
    button.config(state="disabled")
    status.set("Генерація відповіді...")
    output.delete("1.0", "end")
    def worker():
        try:
            data = {"model": "qwen3:4b", "messages": [{"role":"system","content":"Відповідай українською, стисло і точно. Наводь коректний код. Якщо не впевнений, повідом про це."},{"role":"user","content":prompt}], "temperature":0.2,"max_tokens":512,"reasoning_effort":"none","stream":False}
            req=urllib.request.Request("http://localhost:11434/v1/chat/completions",data=json.dumps(data).encode(),headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req,timeout=180) as res:
                answer=json.load(res)["choices"][0]["message"]["content"]
            if not isinstance(answer,str) or not answer.strip():
                raise ValueError("Порожня відповідь моделі")
            root.after(0,lambda: finish(answer,"Готово"))
        except Exception as e:
            msg=str(e)
            root.after(0,lambda: finish("Помилка: "+msg,"Перевірте Ollama, модель та з’єднання."))
    threading.Thread(target=worker,daemon=True).start()

def finish(answer,message):
    output.insert("end",answer)
    status.set(message)
    button.config(state="normal")

root=tk.Tk()
root.title("Локальний помічник програміста")
root.geometry("800x650")
ttk.Label(root,text="Локальний помічник програміста — Qwen3 4B").pack(pady=10)
ttk.Label(root,text="Введіть запит з програмування:").pack()
entry=tk.Text(root,height=6,wrap="word")
entry.pack(fill="x",padx=15,pady=5)
button=ttk.Button(root,text="Отримати відповідь",command=ask)
button.pack(pady=8)
status=tk.StringVar(value="Готовий до роботи")
ttk.Label(root,textvariable=status).pack()
output=tk.Text(root,wrap="word")
output.pack(fill="both",expand=True,padx=15,pady=10)
root.mainloop()
