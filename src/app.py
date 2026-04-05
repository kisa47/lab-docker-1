import os
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

name = os.getenv('USER_NAME', 'Не указано')
group = os.getenv('USER_GROUP', 'Не указана')
port = os.getenv('LISTEN_PORT', 8080)
file_path = os.getenv('SAVED_FILE', './uploads/saved_file.txt')
flsak_debug = os.getenv('FLASK_ENV', 'development')

os.makedirs(os.path.dirname(file_path), exist_ok=True)

template=html = """
    <html>
      <head><title>Данные из переменных окружения</title></head>
      <body>
        <h1>Информация</h1>
        <p>Фамилия и имя (переменная USER_NAME): {{ name }}</p>
        <p>Группа (переменная USER_GROUP): {{ group }}</p>
        <p>Прослушиваемый порт (переменная LISTEN_PORT): {{ port }}</p>
        <p>Файл для хранения данных (переменная SAVED_FILE): {{ file_path }}</p>
        <p>Тип запуска приложения (переменная FLASK_ENV): {{ flsak_debug }}</p>
        <h2>Содержимое файла {{ file_path }}</h2>
        {% if file_content %}
        <pre>{{ file_content }}</pre>
        {% else %}
        <p style="color:red;">{{ file_status }}</p>
        {% endif %}
        <h2>Сохранить текст в файл {{ file_path }}</h2>
        <form method="post" action="{{ url_for('save_file') }}">
            <textarea name="content" rows="10" cols="50" placeholder="Введите текст..."></textarea><br><br>
            <input type="submit" value="Сохранить">
        </form>
      </body>
    </html>
    """
@app.route('/')
def index():
    file_content = None
    file_status = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
    except FileNotFoundError:
        file_status = "Файл не найден. Введите текст и нажмите 'Сохранить'."
    except Exception as e:
        file_status = f"Произошла ошибка при чтении файла: {e}"

    return render_template_string(
        template,
        name=name,
        group=group,
        port=port,
        file_status=file_status,
        file_content=file_content,
        file_path=file_path,
        flsak_debug=flsak_debug
    )

@app.route('/save', methods=['POST'])
def save_file():
    content = request.form.get('content', '').strip()
    if not content:
        return "Пустой текст. Файл не создан.", 400
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return redirect(url_for('index'))
    except Exception as e:
        return f"Ошибка при сохранении файла: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)