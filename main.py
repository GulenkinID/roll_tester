import json
from nicegui import ui, app

json_rolls = "data/rolls.json"

with open(json_rolls, 'r', encoding="utf-8") as f:
    data = json.load(f)
    
rolls = data["rolls"]
roll_names = list(rolls.keys())

class TestState:
    def __init__(self) -> None:
        self.current_index =0
        self.user_inputs = {}
        self.result_text = ""
        
    def reset_for_next(self):
        self.current_index += 1
        self.user_inputs = {}
        self.result_text = ""
        
        
def get_test_state() -> TestState:
    """Возвращает состояние для текущей вкладки, создавая его при необходимости."""
    if 'test_state' not in app.storage.tab:
        app.storage.tab['test_state'] = TestState()
    return app.storage.tab['test_state']


@ui.refreshable
def test_view():
    state = get_test_state()
    
    if state.current_index >= len(roll_names):
        ui.label("Тест Завершён!").classes("text-xl font-bold")
        return
    
    roll_name = roll_names[state.current_index]
    roll = rolls[roll_name]
    
    ui.label(f"Ролл: {roll_name}").classes("text-xl font-bold")
    ui.label(f"Тип: {roll['type']}").classes("text-gray-600")
    
    for item in roll["filling"]:
        
        ui.input(label=f"{item['name']} гр.").bind_value(state.user_inputs, item["name"])
        
    if roll["decoration"]:
        ui.label("Украшение:").classes("text-md font-semibold mt-2")
        for item in roll["decoration"]:
            ui.input(label=f"{item['name']} гр.").bind_value(state.user_inputs, item["name"])
        
    ui.button("Проверить", on_click=lambda: check_answers(state))
    ui.button("Следующий ролл", on_click=next_roll)
    
    if state.result_text:
        ui.label(state.result_text).classes("text-lg")
    

@ui.page('/')
async def main_page():
    await ui.context.client.connected()
    ui.label("Тестирование роллов").classes("text-2xl font-bold")
    test_view()
    
    
def check_answers(state: TestState):
    roll_name = roll_names[state.current_index]
    roll = rolls[roll_name]
    
    results = []
    
    for item in roll['filling']:
        user_value = state.user_inputs.get(item["name"], "").strip()
        correct_value = str(item["grams"])
        
        if user_value == correct_value:
            results.append(f"{item['name']}: верно!")
        else:
            results.append(f"{item['name']}: ошибка (вы ввели {user_value}, правильно {correct_value})")
    if roll['decoration']:    
        for item in roll['decoration']:
            user_value = state.user_inputs.get(item["name"], "").strip()
            correct_value = str(item["grams"])
            
            if user_value == correct_value:
                results.append(f"{item['name']}: верно!")
            else:
                results.append(f"{item['name']}: ошибка (вы ввели {user_value}, правильно {correct_value})")
            
    state.result_text = "\n".join(results)
    test_view.refresh()


def next_roll():
    state = get_test_state()
    state.reset_for_next()
    test_view.refresh()
    
    
ui.run(port=8082, storage_secret="secret_string")

# ui.label("Тестирование роллов").classes("text-2x1 font-bold text-center w-full")

# for name, roll in rolls.items():
#     with ui.expansion(name).classes("w-full border rounded-lg mb-2"):
#         ui.label(f"Тип: {roll["type"]}").classes("font-bold")
#         ui.label("Начинка:")
#         for item in roll["filling"]:
#             ui.label(f"  {item["name"]} - {item["grams"]} гр.")
#         if roll["decoration"]:
#             ui.label(f"Украшение:").classes("font-bold")
#             for item in roll["decoration"]:
#                 ui.label(f"  {item["name"]} - {item["grams"]} гр.")
                    
            
# ui.run()