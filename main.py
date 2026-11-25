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
        self.results = []
        
    def reset_for_next(self):
        self.current_index += 1
        self.user_inputs = {}
        self.results = []
        
        
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
    
    if state.results:
        for text, is_correct in state.results:
            color = "text-green-600" if is_correct else "text-red-600"
            ui.label(text).classes(f"text-lg {color}")
    

@ui.page('/')
async def main_page():
    await ui.context.client.connected()
    ui.label("Тестирование роллов").classes("text-2xl font-bold")
    test_view()
    
    
def check_answers(state: TestState):
    roll_name = roll_names[state.current_index]
    roll = rolls[roll_name]
    
    state.results = []
    
    for item in roll['filling']:
        user_value = state.user_inputs.get(item["name"], "").strip()
        correct_value = str(item["grams"])
        is_correct = user_value == correct_value
        
        if is_correct:
            text = f"{item['name']}: верно!"
        else:
            text = f"{item['name']}: ошибка (вы ввели {user_value}, правильно {correct_value})"
        state.results.append((text, is_correct))
    if roll['decoration']:    
        for item in roll['decoration']:
            user_value = state.user_inputs.get(item["name"], "").strip()
            correct_value = str(item["grams"])
            is_correct = user_value == correct_value
            
            if is_correct:
                text = f"{item['name']}: верно!"
            else:
                text = f"{item['name']}: ошибка (вы ввели {user_value}, правильно {correct_value})"
                
            state.results.append((text, is_correct))
            
    # state.results = "\n".join(results)
    test_view.refresh()


def next_roll():
    state = get_test_state()
    state.reset_for_next()
    test_view.refresh()
    
    
ui.run(port=8082, storage_secret="secret_string")