from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random


def captcha_check():
    """Функция показывает капчу и возвращает True/False"""

    result = {'value': False}

    def check():
        # Получаем введенную строку
        user_input = entry_order.get().strip()

        # Проверяем что введено
        if not user_input:
            messagebox.showerror("Ошибка!", "Введите порядок номеров!")
            return

        # Проверяем что введено "1234"
        if user_input == "1234":
            result['value'] = True
            messagebox.showinfo("Успех!", "✅ Капча пройдена!")
            window.destroy()
        else:
            messagebox.showerror("Ошибка!", f"❌ Неправильно!\nПравильный порядок: 1234\nВы ввели: {user_input}")

    def shuffle():
        positions = list(range(4))
        random.shuffle(positions)
        for i, piece in enumerate(pieces):
            piece['pos'] = positions[i]
        show_puzzle()

    def on_click(event):
        nonlocal selected_pos
        col = event.x // 150
        row = event.y // 150

        if col < 2 and row < 2:
            clicked_pos = row * 2 + col

            if selected_pos is None:
                selected_pos = clicked_pos
                canvas.create_rectangle(col * 150, row * 150, (col + 1) * 150, (row + 1) * 150,
                                        outline='red', width=4, tags="highlight")
            else:
                if selected_pos != clicked_pos:
                    for p in pieces:
                        if p['pos'] == selected_pos:
                            p['pos'] = clicked_pos
                        elif p['pos'] == clicked_pos:
                            p['pos'] = selected_pos
                    show_puzzle()
                canvas.delete("highlight")
                selected_pos = None

    def show_puzzle():
        canvas.delete("all")
        # Рисуем сетку 2x2
        for i in range(1, 3):
            canvas.create_line(0, i * 150, 300, i * 150, fill='black', width=2)
            canvas.create_line(i * 150, 0, i * 150, 300, fill='black', width=2)

        for piece in pieces:
            row = piece['pos'] // 2
            col = piece['pos'] % 2
            x, y = col * 150 + 5, row * 150 + 5
            canvas.create_image(x, y, image=piece['img'], anchor="nw")
            canvas.create_text(x + 70, y + 70, text=str(piece['id'] + 1),
                               fill='white', font=('Arial', 20, 'bold'))

    # Создаем окно
    window = Tk()
    window.geometry("450x650")
    window.title("Капча - Пазл")

    Label(window, text="ПРОСТАЯ КАПЧА", font=("Arial", 18, "bold"),
          fg="darkblue").pack(pady=10)
    Label(window, text="Кликните на две части, чтобы поменять их местами",
          font=("Arial", 10)).pack()

    canvas = Canvas(window, width=300, height=300,
                    bg='lightgray', bd=2, relief="solid")
    canvas.pack(pady=20)

    Label(window, text="Введите правильный порядок номеров (без запятых):",
          font=("Arial", 10, "bold")).pack()

    entry_order = Entry(window, font=("Arial", 14), justify='center', width=15)
    entry_order.pack(pady=5)

    Label(window, text="Пример: 1234", font=("Arial", 9), fg="blue").pack()

    Button(window, text="✅ Проверить", command=check,
           bg="green", fg="white", font=("Arial", 12), width=15).pack(pady=10)

    Button(window, text="🔄 Перемешать", command=shuffle,
           bg="orange", font=("Arial", 10), width=15).pack()

    # Загружаем картинки
    pieces = []
    for i in range(4):
        try:
            img = Image.open(f"images/{i + 1}.png")
            img = img.resize((140, 140), Image.Resampling.LANCZOS)
            pieces.append({
                'id': i, 'correct': i, 'pos': i,
                'img': ImageTk.PhotoImage(img)
            })
        except:
            img = Image.new('RGB', (140, 140), color=['red', 'green', 'blue', 'yellow'][i])
            pieces.append({
                'id': i, 'correct': i, 'pos': i,
                'img': ImageTk.PhotoImage(img)
            })

    selected_pos = None
    shuffle()

    canvas.bind("<Button-1>", on_click)

    # Нажатие Enter в поле ввода
    entry_order.bind('<Return>', lambda e: check())

    window.wait_window()
    return result['value']


# Использование
if __name__ == "__main__":
    if captcha_check():
        print("True - капча пройдена!")
    else:
        print("False - капча не пройдена!")