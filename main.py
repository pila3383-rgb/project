import random
import tkinter as tk
from tkinter import messagebox

# --- Графическая тема (Цветовая палитра) ---
BG_MAIN = "#1a1a2e"
BG_CARD = "#16213e"
TEXT_COLOR = "#e9eff1"
ACCENT_GREEN = "#0f9755"
ACCENT_BLUE = "#0f8694"
HOVER_BLUE = "#0a5d68"
ACCENT_ORANGE = "#d97706"

# Профиль пользователя
COURIERS = {"name": "Иван Петров (Вы)", "phone": "+7 (999) 123-45-67"}

# База случайных адресов для автогенерации
ADDRESSES = [
    "ул. Ленина, д. 12, кв. 45",
    "пр. Мира, д. 8, кв. 102",
    "ул. Пушкина, д. 24, кв. 17",
    "ул. Гагарина, д. 5, кв. 89",
    "ул. Чехова, д. 14, кв. 3",
    "ул. Кирова, д. 51, кв. 66",
    "Привокзальная пл., д. 2",
]

# База случайных имён клиентов
CLIENT_NAMES = [
    "Александр",
    "Мария",
    "Дмитрий",
    "Анна",
    "Максим",
    "Елена",
    "Артём",
    "Ольга",
    "Сергей",
    "Татьяна",
    "Игорь",
    "Наталья",
    "Aлексей",
    "Юлия",
    "Владимир",
]


class CourierApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Courier Delivery Tracker")
        self.geometry("540x600")
        self.configure(bg=BG_MAIN)

        # Хранилище данных о курьерах для заказов
        self.order_couriers = {}

        # Заголовок приложения
        self.header = tk.Label(
            self,
            text="Трекер доставки заказов",
            font=("Arial", 16, "bold"),
            bg=BG_MAIN,
            fg=TEXT_COLOR,
        )
        self.header.pack(pady=15)

        # --- Список заказов ---
        self.list_frame = tk.Frame(self, bg=BG_MAIN)
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.orders_list = tk.Listbox(
            self.list_frame,
            font=("Arial", 10),
            bg=BG_CARD,
            fg=TEXT_COLOR,
            selectbackground="#30475e",
            selectforeground=TEXT_COLOR,
            bd=0,
            highlightthickness=0,
            activestyle="none",
        )
        self.orders_list.pack(side="left", fill="both", expand=True)
        self.orders_list.bind("<<ListboxSelect>>", self.on_select_order)

        self.scrollbar = tk.Scrollbar(
            self.list_frame, orient="vertical", command=self.orders_list.yview
        )
        self.scrollbar.pack(side="right", fill="y")
        self.orders_list.config(yscrollcommand=self.scrollbar.set)

        # --- ИНФОРМАЦИЯ О ДОСТАВЩИКЕ ---
        self.courier_frame = tk.LabelFrame(
            self,
            text=" 📋 Информация о доставщике ",
            font=("Arial", 10, "bold"),
            bg=BG_CARD,
            fg=ACCENT_BLUE,
            bd=1,
            padx=10,
            pady=10,
        )
        self.courier_frame.pack(fill="x", padx=20, pady=10)

        self.courier_info_label = tk.Label(
            self.courier_frame,
            text="Выберите заказ на складе и заберите его лично...",
            font=("Arial", 10, "italic"),
            bg=BG_CARD,
            fg="#a0aec0",
            justify="left",
        )
        self.courier_info_label.pack(anchor="w")

        # --- Блок управления статусами ---
        self.actions_frame = tk.Frame(self, bg=BG_MAIN)
        self.actions_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Кнопка «Взять заказ»
        self.take_btn = tk.Button(
            self.actions_frame,
            text="➕ Взять заказ в работу",
            font=("Arial", 11, "bold"),
            bg=ACCENT_BLUE,
            fg=TEXT_COLOR,
            activebackground=HOVER_BLUE,
            activeforeground=TEXT_COLOR,
            bd=0,
            cursor="hand2",
            command=self.take_order_manually,
            pady=10,
        )
        self.take_btn.pack(fill="x", side="top", pady=(0, 8))

        # Кнопка «Выполнено»
        self.done_btn = tk.Button(
            self.actions_frame,
            text="✓ Подтвердить: Доставлено",
            font=("Arial", 11, "bold"),
            bg=ACCENT_GREEN,
            fg=TEXT_COLOR,
            activebackground="#0b7340",
            activeforeground=TEXT_COLOR,
            bd=0,
            cursor="hand2",
            command=self.complete_order,
            pady=10,
        )
        self.done_btn.pack(fill="x", side="top")

        # Запуск процессов
        self.auto_incoming_orders()
        self.auto_delivery_transit()

    # Процесс: Новые заказы поступают на склад автоматически
    def auto_incoming_orders(self):
        order_num = random.randint(1000, 9999)
        client = random.choice(CLIENT_NAMES)
        order_id = f"Заказ #{order_num} (Клиент: {client})"
        self.orders_list.insert(tk.END, f" 📦 [Прибыл на склад] {order_id}")

        next_delay = random.randint(5000, 10000)
        self.after(next_delay, self.auto_incoming_orders)

    # Действие человека: Сам нажимает кнопку и берет заказ в работу
    def take_order_manually(self):
        selected_index = self.orders_list.curselection()
        if not selected_index:
            messagebox.showwarning(
                "Внимание", "Выберите заказ со склада, который хотите взять!"
            )
            return

        idx = selected_index[0]  # Получаем числовое значение индекса из кортежа
        current_text = self.orders_list.get(idx)

        if "📦 [Прибыл на склад]" in current_text:
            order_id = current_text.replace(" 📦 [Прибыл на склад] ", "")
            new_text = f" 📋 [Заказ взят] {order_id}"

            # Назначаем исполнителя безопасным образом
            self.order_couriers[new_text] = COURIERS

            self.orders_list.delete(idx)
            self.orders_list.insert(idx, new_text)
            self.orders_list.selection_set(idx)
            self.on_select_order(None)
        else:
            messagebox.showinfo("Инфо", "Этот заказ уже взят или доставлен!")

    # Фаза 2: Автоматический переход из [Заказ взят] -> [Идет доставка]
    def auto_delivery_transit(self):
        # Копируем элементы, чтобы безопасно определять актуальные индексы
        items = list(self.orders_list.get(0, tk.END))

        for text in items:
            if "📋 [Заказ взят]" in text:
                # Находим актуальный индекс элемента в Listbox
                try:
                    idx = self.orders_list.get(0, tk.END).index(text)
                except ValueError:
                    continue

                order_id = text.replace(" 📋 [Заказ взят] ", "")
                random_address = random.choice(ADDRESSES)
                new_text = (
                    f" 🚚 [Идет доставка] {order_id} -> {random_address}"
                )

                # Переносим данные курьера на новый ключ статуса
                if text in self.order_couriers:
                    self.order_couriers[new_text] = self.order_couriers.pop(
                        text
                    )
                else:
                    self.order_couriers[new_text] = COURIERS

                is_selected = self.orders_list.selection_includes(idx)

                self.orders_list.delete(idx)
                self.orders_list.insert(idx, new_text)

                if is_selected:
                    self.orders_list.selection_set(idx)
                    self.on_select_order(None)
                break

        next_delay = random.randint(3000, 5000)
        self.after(next_delay, self.auto_delivery_transit)

    # Обновление карточки курьера при клике
    def on_select_order(self, event):
        selected_index = self.orders_list.curselection()
        if not selected_index:
            return

        idx = selected_index[0]
        current_text = self.orders_list.get(idx)

        if (
            "📋 [Заказ взят]" in current_text
            and current_text in self.order_couriers
        ):
            courier = self.order_couriers[current_text]
            self.courier_info_label.config(
                text=f"Курьер: {courier['name']}\nТелефон: {courier['phone']}\nСтатус: Вы взяли заказ. Собираетесь на склад.",
                fg=ACCENT_ORANGE,
            )
        elif (
            "🚚 [Идет доставка]" in current_text
            and current_text in self.order_couriers
        ):
            courier = self.order_couriers[current_text]
            self.courier_info_label.config(
                text=f"Курьер: {courier['name']}\nТелефон: {courier['phone']}\nСтатус: Вы в пути к клиенту.",
                fg=TEXT_COLOR,
            )
        elif "✅ [Доставлен]" in current_text:
            self.courier_info_label.config(
                text="Вы успешно доставили этот заказ!\n(Удаление из истории через 3 секунды...)",
                fg=ACCENT_GREEN,
            )
        else:
            self.courier_info_label.config(
                text="Заказ на складе. Нажмите «Взять заказ в работу»",
                fg="#a0aec0",
            )

    # Ручное подтверждение доставки -> [Доставлен]
    def complete_order(self):
        selected_index = self.orders_list.curselection()
        if not selected_index:
            messagebox.showwarning(
                "Внимание", "Выберите заказ, чтобы отметить его как доставленный!"
            )
            return

        idx = selected_index[0]
        current_text = self.orders_list.get(idx)

        if (
            "🚚 [Идет доставка]" in current_text
            or "📋 [Заказ взят]" in current_text
        ):
            old_tag = (
                "🚚 [Идет доставка]"
                if "🚚 [Идет доставка]" in current_text
                else "📋 [Заказ взят]"
            )
            new_text = current_text.replace(old_tag, "✅ [Доставлен]")

            if current_text in self.order_couriers:
                self.order_couriers[new_text] = self.order_couriers.pop(
                    current_text
                )

            self.orders_list.delete(idx)
            self.orders_list.insert(idx, new_text)
            self.orders_list.selection_set(idx)
            self.on_select_order(None)

            # Таймер автоудаления (3 секунды)
            self.after(3000, lambda: self.auto_delete_callback(new_text))

        elif "📦 [Прибыл на склад]" in current_text:
            messagebox.showinfo(
                "Инфо",
                "Вы еще не взяли этот заказ! Сначала нажмите «Взять заказ в работу»",
            )
        else:
            messagebox.showinfo("Инфо", "Этот заказ уже доставлен!")

    # Фоновое удаление доставленного заказа
    def auto_delete_callback(self, text_to_delete):
        all_items = self.orders_list.get(0, tk.END)
        if text_to_delete in all_items:
            idx = all_items.index(text_to_delete)

            if text_to_delete in self.order_couriers:
                del self.order_couriers[text_to_delete]

            is_selected = self.orders_list.selection_includes(idx)
            self.orders_list.delete(idx)

            if is_selected:
                self.courier_info_label.config(
                    text="Выберите заказ из списка для просмотра деталей",
                    fg="#a0aec0",
                )


if __name__ == "__main__":
    app = CourierApp()
    app.mainloop()
